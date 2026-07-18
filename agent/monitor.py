from __future__ import annotations

import json
import os
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

from projects import ProjectConfig, load_projects
from storage import MonitorStore
from capabilities import extract_capability_events, load_capabilities, render_capability_matrix
from project_detail import write_project_detail
from evolution_brief import write_evolution_brief

AGENT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = AGENT_DIR.parent
STATE_PATH = AGENT_DIR / "state.json"
PROJECTS_PATH = SKILL_ROOT / "config" / "projects.json"
CAPABILITIES_PATH = SKILL_ROOT / "config" / "capabilities.json"
DATABASE_PATH = SKILL_ROOT / "data" / "monitor.db"
REQUEST_TIMEOUT = 10
USER_AGENT = "inference-framework-monitor/0.2"


def _local_now() -> datetime:
    return datetime.now().astimezone()


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _request_json(session: requests.Session, url: str, params: dict[str, Any] | None = None) -> Any:
    response = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def _build_commit_window(run_date: date, local_tz: timezone) -> dict[str, str]:
    start = datetime.combine(run_date, time.min, tzinfo=local_tz)
    end = start + timedelta(days=1) - timedelta(seconds=1)
    return {
        "local_date": run_date.isoformat(),
        "local_start": start.isoformat(),
        "local_end": end.isoformat(),
        "since_utc": start.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "until_utc": end.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def _safe_request(callable_: Any, label: str, errors: list[str]) -> Any:
    try:
        return callable_()
    except requests.RequestException as exc:
        errors.append(f"{label}: {exc}")
        return None


def _get_pypi(session: requests.Session, package: str, errors: list[str]) -> dict[str, Any]:
    data = _safe_request(lambda: _request_json(session, f"https://pypi.org/pypi/{package}/json"), f"PyPI {package}", errors)
    info = data.get("info", {}) if isinstance(data, dict) else {}
    return {"version": info.get("version"), "package_url": info.get("package_url")}


def _get_release(session: requests.Session, repo: str, errors: list[str]) -> dict[str, Any]:
    data = _safe_request(
        lambda: _request_json(session, f"https://api.github.com/repos/{repo}/releases/latest"),
        f"GitHub release {repo}",
        errors,
    )
    if not isinstance(data, dict):
        return {}
    return {key: data.get(key) for key in ("tag_name", "name", "published_at", "html_url", "body")}


def _get_release_catalog(session: requests.Session, repo: str, errors: list[str]) -> list[dict[str, Any]]:
    """Fetch up to 300 non-draft releases for historical Feature timelines."""
    releases: list[dict[str, Any]] = []
    for page in range(1, 4):
        data = _safe_request(
            lambda page=page: _request_json(session, f"https://api.github.com/repos/{repo}/releases", {"per_page": 100, "page": page}),
            f"GitHub release catalog {repo}",
            errors,
        )
        if not isinstance(data, list):
            break
        releases.extend(
            item for item in data
            if isinstance(item, dict)
            and not item.get("draft")
            and not item.get("prerelease")
            and str(item.get("tag_name") or "").startswith("v")
        )
        if len(data) < 100:
            break
    return [{key: item.get(key) for key in ("tag_name", "name", "published_at", "html_url", "body")} for item in releases]


def _get_commits(session: requests.Session, repo: str, window: dict[str, str], errors: list[str]) -> list[dict[str, Any]]:
    data = _safe_request(
        lambda: _request_json(session, f"https://api.github.com/repos/{repo}/commits", {"since": window["since_utc"], "until": window["until_utc"], "per_page": 100}),
        f"GitHub commits {repo}",
        errors,
    )
    if not isinstance(data, list):
        return []
    commits: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        commit = item.get("commit") if isinstance(item.get("commit"), dict) else {}
        committer = commit.get("committer") if isinstance(commit.get("committer"), dict) else {}
        message = str(commit.get("message") or "").strip()
        commits.append({"sha": item.get("sha"), "short_sha": str(item.get("sha") or "")[:7], "title": message.splitlines()[0] if message else "No message", "committed_at": committer.get("date"), "url": item.get("html_url")})
    return commits


def _get_issues(session: requests.Session, repo: str, errors: list[str]) -> list[dict[str, Any]]:
    data = _safe_request(
        lambda: _request_json(session, f"https://api.github.com/repos/{repo}/issues", {"sort": "comments", "direction": "desc", "state": "open", "per_page": 5}),
        f"GitHub issues {repo}",
        errors,
    )
    if not isinstance(data, list):
        return []
    return [{"number": item.get("number"), "title": item.get("title"), "comments": item.get("comments", 0), "url": item.get("html_url"), "type": "pull_request" if isinstance(item.get("pull_request"), dict) else "issue"} for item in data if isinstance(item, dict)]


def _version_entry(current: str | None, previous: str | None, **metadata: Any) -> dict[str, Any]:
    return {"current": current, "previous": previous, "changed": bool(current and previous and current != previous), **metadata}


def _collect_project(
    session: requests.Session,
    project: ProjectConfig,
    window: dict[str, str],
    store: MonitorStore,
    cursor: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    previous = store.latest_versions(project.id)
    # CI runners may start without the local SQLite history. state.json is the
    # portable cursor in that case; SQLite remains the complete local history.
    cursor_projects = cursor.get("projects") if isinstance(cursor.get("projects"), dict) else {}
    cursor_project = cursor_projects.get(project.id) if isinstance(cursor_projects.get(project.id), dict) else {}
    previous["pypi_version"] = previous["pypi_version"] or cursor_project.get("pypi_version")
    previous["github_release_version"] = previous["github_release_version"] or cursor_project.get("github_release_version")
    pypi = _get_pypi(session, project.pypi_package, errors) if project.pypi_package else {}
    release = _get_release(session, project.github_repo, errors)
    release_catalog = _get_release_catalog(session, project.github_repo, errors)
    commits = _get_commits(session, project.github_repo, window, errors)
    issues = _get_issues(session, project.github_repo, errors)
    return {
        "id": project.id,
        "name": project.name,
        "github_repo": project.github_repo,
        "versions": {
            "pypi": _version_entry(pypi.get("version"), previous["pypi_version"], package_url=pypi.get("package_url")),
            "github_release": _version_entry(release.get("tag_name"), previous["github_release_version"], html_url=release.get("html_url"), published_at=release.get("published_at"), name=release.get("name")),
        },
        "latest_release_notes": release.get("body"),
        "release_catalog": release_catalog,
        "daily_commits": commits,
        "daily_commit_count": len(commits),
        "popular_issues": issues,
        "popular_issue_count": len(issues),
        "errors": errors,
    }


def _save_cursor(run_at: datetime, window: dict[str, str], projects: list[dict[str, Any]]) -> None:
    _write_json(STATE_PATH, {"last_run_date": run_at.date().isoformat(), "last_collected_at": run_at.isoformat(), "timezone": str(run_at.tzinfo or timezone.utc), "last_commit_window": window, "projects": {project["id"]: {"pypi_version": project["versions"]["pypi"]["current"], "github_release_version": project["versions"]["github_release"]["current"], "tracked_issues": [issue["number"] for issue in project["popular_issues"] if issue.get("number") is not None], "last_errors": project["errors"]} for project in projects}})


def monitor_all() -> dict[str, Any]:
    """Collect a normalized snapshot for every configured inference framework."""
    run_at = _local_now()
    local_tz = run_at.tzinfo or timezone.utc
    window = _build_commit_window(run_at.date(), local_tz)
    projects = load_projects(PROJECTS_PATH)
    capabilities = load_capabilities(CAPABILITIES_PATH)
    store = MonitorStore(DATABASE_PATH)
    cursor = _read_json(STATE_PATH)
    cursor = cursor if isinstance(cursor, dict) else {}
    with requests.Session() as session:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"
        session.headers.update(headers)
        snapshots = [_collect_project(session, project, window, store, cursor) for project in projects]
    capability_events: list[dict[str, Any]] = []
    for snapshot in snapshots:
        for catalog_release in sorted(snapshot["release_catalog"], key=lambda item: str(item.get("published_at") or "")):
            release_events = extract_capability_events(
                {
                    "id": snapshot["id"],
                    "name": snapshot["name"],
                    "versions": {"github_release": {"current": catalog_release.get("tag_name"), "html_url": catalog_release.get("html_url")}},
                    "latest_release_notes": catalog_release.get("body") or "",
                },
                capabilities,
            )
            capability_events.extend({**event, "release_published_at": catalog_release.get("published_at")} for event in release_events)
    store.save_run(
        collected_at=run_at.isoformat(), timezone=str(local_tz), commit_window=window,
        projects=snapshots, capability_events=capability_events,
    )
    _save_cursor(run_at, window, snapshots)
    detail_paths = [
        write_project_detail(SKILL_ROOT / "reports" / "projects" / f"{snapshot['id']}.md", snapshot, snapshot["release_catalog"], capabilities)
        for snapshot in snapshots
    ]
    brief_paths = [
        write_evolution_brief(SKILL_ROOT / "reports" / "briefs" / f"{snapshot['id']}.md", snapshot, snapshot["release_catalog"], capabilities, run_at.date().isoformat())
        for snapshot in snapshots
    ]

    # Compatibility layer for the existing vLLM-focused report renderer.
    primary = next((project for project in snapshots if project["id"] == "vllm"), snapshots[0])
    pypi = primary["versions"]["pypi"]
    release = primary["versions"]["github_release"]
    changes = [f"{project['name']}: {source} {entry['previous']} -> {entry['current']}" for project in snapshots for source, entry in (("PyPI", project["versions"]["pypi"]), ("GitHub release", project["versions"]["github_release"])) if entry["changed"]]
    matrix = store.latest_capability_matrix()
    report_projects = [{key: value for key, value in snapshot.items() if key != "release_catalog"} for snapshot in snapshots]
    return {"date": run_at.date().isoformat(), "collected_at": run_at.isoformat(), "timezone": str(local_tz), "commit_window": window, "projects": report_projects, "project_detail_reports": [str(path.relative_to(SKILL_ROOT)) for path in detail_paths], "evolution_briefs": [str(path.relative_to(SKILL_ROOT)) for path in brief_paths], "capability_events": capability_events, "capability_matrix_markdown": render_capability_matrix(snapshots, capabilities, matrix), "changes_detected": bool(changes), "change_items": changes, "pypi_version": pypi["current"], "github_version": release["current"], "versions": primary["versions"], "daily_commits": primary["daily_commits"], "daily_commit_count": primary["daily_commit_count"], "popular_issues": primary["popular_issues"], "popular_issue_count": primary["popular_issue_count"], "errors": [error for project in snapshots for error in project["errors"]]}


if __name__ == "__main__":
    from report import generate_report

    data = monitor_all()
    print(f"Collected {len(data['projects'])} projects; {len(data['errors'])} source errors.")
    print(f"Report saved to: {generate_report(data)}")
