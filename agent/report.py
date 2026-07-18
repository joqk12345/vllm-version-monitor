from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

AGENT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = AGENT_DIR.parent
REPORTS_DIR = SKILL_ROOT / "reports"
README_PATH = SKILL_ROOT / "README.md"
CHANGELOG_PATH = SKILL_ROOT / "CHANGELOG.md"
STATE_PATH = AGENT_DIR / "state.json"

PIPELINE_LOG_PATH = Path("/tmp/pipeline-log.json")
CHANGE_REPORT_PATH = Path("/tmp/change-report.json")
VERIFY_REPORT_PATH = Path("/tmp/verify-report.json")
COST_LOG_PATH = Path("/tmp/agent-costs.json")
SYSTEM_PROMPT_PATH = AGENT_DIR / "report-prompt.md"


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _read_json(path: Path) -> Any:
    raw = _read_text(path)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _read_required_text(path: Path, label: str) -> str:
    text = _read_text(path)
    if text is None:
        raise FileNotFoundError(f"Could not read {label} at {path}")
    return text


def _run_git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=SKILL_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _normalize_status(value: Any) -> str:
    raw = str(value or "unknown").strip().lower()
    mapping = {
        "ok": "success",
        "passed": "success",
        "completed": "success",
        "succeeded": "success",
        "error": "failed",
        "fail": "failed",
        "skipped": "skipped",
        "in_progress": "running",
    }
    return mapping.get(raw, raw)


def _format_duration(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, (int, float)):
        if value >= 60:
            return f"{value / 60:.1f}m"
        if value >= 1:
            return f"{int(value)}s"
        return f"{value:.2f}s"
    text = str(value).strip()
    return text or "—"


def _tail(text: str | None, lines: int = 12) -> str:
    if not text:
        return "N/A"
    chunks = text.strip().splitlines()
    if not chunks:
        return "N/A"
    return "\n".join(chunks[-lines:])


def _extract_steps(pipeline_log: Any, fallback_data: dict[str, Any]) -> list[dict[str, Any]]:
    raw_steps: list[Any] = []

    if isinstance(pipeline_log, dict):
        steps = pipeline_log.get("steps")
        if isinstance(steps, list):
            raw_steps = steps
        elif isinstance(steps, dict):
            raw_steps = [{"name": key, **(value if isinstance(value, dict) else {})} for key, value in steps.items()]

    normalized: list[dict[str, Any]] = []
    for step in raw_steps:
        if isinstance(step, str):
            normalized.append(
                {
                    "name": step,
                    "result": "unknown",
                    "duration": None,
                    "notes": "",
                    "exit_code": None,
                    "last_output": None,
                }
            )
            continue

        if not isinstance(step, dict):
            continue

        name = step.get("name") or step.get("step") or "Unknown"
        result = _normalize_status(step.get("result") or step.get("status") or step.get("outcome"))
        duration = step.get("duration") or step.get("durationSec") or step.get("durationSeconds")
        notes = (
            step.get("notes")
            or step.get("note")
            or step.get("message")
            or step.get("error")
            or step.get("summary")
            or ""
        )
        normalized.append(
            {
                "name": str(name),
                "result": result,
                "duration": duration,
                "notes": str(notes),
                "exit_code": step.get("exitCode") or step.get("exit_code"),
                "last_output": step.get("lastOutput") or step.get("output"),
            }
        )

    if normalized:
        return normalized

    monitor_status = "success" if fallback_data else "unknown"
    return [
        {
            "name": "Monitor",
            "result": monitor_status,
            "duration": None,
            "notes": "Collected upstream version, commits and issue activity.",
            "exit_code": None,
            "last_output": None,
        },
        {
            "name": "Report",
            "result": "success",
            "duration": None,
            "notes": "Daily report generated.",
            "exit_code": None,
            "last_output": None,
        },
    ]


def _extract_change_items(change_report: Any) -> list[str]:
    if not isinstance(change_report, dict):
        return []

    changes = change_report.get("changes")
    if isinstance(changes, list):
        values: list[str] = []
        for item in changes:
            if isinstance(item, str):
                values.append(item)
            elif isinstance(item, dict):
                kind = item.get("type") or item.get("kind") or item.get("name")
                detail = item.get("detail") or item.get("message") or item.get("value")
                if kind and detail:
                    values.append(f"{kind}: {detail}")
                elif kind:
                    values.append(str(kind))
        return values

    if isinstance(changes, dict):
        values = []
        for key, value in changes.items():
            values.append(f"{key}: {value}")
        return values

    return []


def _detect_changes(data: dict[str, Any], change_report: Any) -> tuple[bool | None, list[str]]:
    items = _extract_change_items(change_report)
    payload_items = _coerce_change_items(data)
    if payload_items:
        items = payload_items + [item for item in items if item not in payload_items]

    if isinstance(change_report, dict):
        marker = (
            change_report.get("changes_detected")
            if "changes_detected" in change_report
            else change_report.get("changeDetected")
        )
        if isinstance(marker, bool):
            return marker, items

    payload_marker = data.get("changes_detected")
    if isinstance(payload_marker, bool):
        return payload_marker, items

    for key, fallback_key in (("pypi", "pypi_version"), ("github_release", "github_version")):
        entry = _version_entry(data, key, fallback_key)
        if entry.get("changed") is True:
            return True, items
        if entry.get("changed") is False and entry.get("current"):
            continue

    comparison = str(data.get("version_comparison") or "").lower()
    if comparison:
        if "无法比较" in comparison or "cannot compare" in comparison:
            return None, items
        if "无变化" in comparison or "no change" in comparison:
            return False, items
        return True, items

    return (True if items else None), items


def _find_step(steps: list[dict[str, Any]], keyword: str) -> dict[str, Any] | None:
    key = keyword.lower()
    for step in steps:
        name = str(step.get("name", "")).lower()
        if key in name:
            return step
    return None


def _read_related_log(step_name: str) -> str | None:
    name = step_name.lower()
    mapping = {
        "update": Path("/tmp/update-agent.log"),
        "research (ts)": Path("/tmp/research-ts.log"),
        "research (py)": Path("/tmp/research-py.log"),
        "research": Path("/tmp/research-py.log"),
        "verify": Path("/tmp/verify.log"),
    }
    for key, path in mapping.items():
        if key in name:
            return _read_text(path)

    if "mending" in name:
        candidates = sorted(Path("/tmp").glob("mending-agent-*.log"))
        if candidates:
            return _read_text(candidates[-1])
    return None


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except ValueError:
        return None


def _money(value: float | None, strong: bool = False, unavailable: str = "N/A") -> str:
    if value is None:
        return unavailable
    amount = f"${value:.2f}"
    return f"**{amount}**" if strong else amount


def _extract_cost_rows(cost_log: Any) -> tuple[list[dict[str, Any]], float | None]:
    rows: list[dict[str, Any]] = []

    if isinstance(cost_log, list):
        for item in cost_log:
            if not isinstance(item, dict):
                continue
            agent = item.get("agent") or item.get("name")
            cost = _safe_float(item.get("costUsd") or item.get("cost_usd") or item.get("total_cost_usd"))
            turns = item.get("turns")
            if agent:
                rows.append({"agent": str(agent), "cost": cost, "turns": turns})
    elif isinstance(cost_log, dict):
        source = cost_log.get("agents") if isinstance(cost_log.get("agents"), dict) else cost_log
        for key, value in source.items():
            if not isinstance(value, dict):
                continue
            cost = _safe_float(value.get("costUsd") or value.get("cost_usd") or value.get("total_cost_usd"))
            turns = value.get("turns")
            rows.append({"agent": str(key), "cost": cost, "turns": turns})

    numeric_costs = [entry["cost"] for entry in rows if isinstance(entry.get("cost"), float)]
    total = sum(numeric_costs) if numeric_costs else None
    return rows, total


def _count_lines(prefix: str, value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    text = str(value or "")
    return sum(1 for line in text.splitlines() if line.strip().startswith(prefix))


def _version_entry(data: dict[str, Any], key: str, fallback_key: str) -> dict[str, Any]:
    versions = data.get("versions")
    if isinstance(versions, dict):
        entry = versions.get(key)
        if isinstance(entry, dict):
            return entry
    return {"current": data.get(fallback_key), "previous": None, "changed": None}


def _coerce_change_items(data: dict[str, Any]) -> list[str]:
    raw = data.get("change_items")
    if not isinstance(raw, list):
        return []
    return [str(item) for item in raw if item]


def _daily_commit_count(data: dict[str, Any]) -> int:
    explicit_count = data.get("daily_commit_count")
    if isinstance(explicit_count, int):
        return explicit_count
    return _count_lines("-", data.get("daily_commits_markdown") or data.get("daily_commits"))


def _issue_count(data: dict[str, Any]) -> int:
    explicit_count = data.get("popular_issue_count")
    if isinstance(explicit_count, int):
        return explicit_count
    return _count_lines("- #", data.get("popular_issues_markdown") or data.get("popular_issues"))


def _derive_summary(
    steps: list[dict[str, Any]],
    data: dict[str, Any],
    changes_detected: bool | None,
) -> str:
    failures = [step for step in steps if step.get("result") == "failed"]
    if failures:
        names = ", ".join(step.get("name", "Unknown") for step in failures)
        return f"Pipeline finished with failures in: {names}. See Errors section for details."
    collection_errors = data.get("errors")
    if isinstance(collection_errors, list) and collection_errors:
        return f"Monitoring finished with {len(collection_errors)} upstream collection errors. See Errors section; version conclusions may be incomplete."

    pypi = _version_entry(data, "pypi", "pypi_version")
    github = _version_entry(data, "github_release", "github_version")
    if changes_detected is False:
        return "No upstream changes were detected. The monitor captured a baseline snapshot."
    changed_versions: list[str] = []
    for label, entry in (("PyPI", pypi), ("GitHub release", github)):
        if entry.get("changed") is True and entry.get("current"):
            previous = entry.get("previous")
            current = entry.get("current")
            if previous:
                changed_versions.append(f"{label} moved from `{previous}` to `{current}`")
            else:
                changed_versions.append(f"{label} is now tracked at `{current}`")
    if changed_versions:
        return "Monitoring completed successfully. " + "; ".join(changed_versions) + "."
    if pypi.get("current") or github.get("current"):
        return (
            "Monitoring completed successfully. "
            f"Latest versions: PyPI `{pypi.get('current') or 'N/A'}`, GitHub `{github.get('current') or 'N/A'}`."
        )
    return "Monitoring completed successfully and report artifacts were refreshed."


def _build_report(
    date: str,
    data: dict[str, Any],
    pipeline_log: Any,
    change_report: Any,
    verify_report: Any,
    cost_log: Any,
    state_data: Any,
) -> tuple[str, str, dict[str, Any]]:
    steps = _extract_steps(pipeline_log, data)
    changes_detected, change_items = _detect_changes(data, change_report)
    summary = _derive_summary(steps, data, changes_detected)
    pypi = _version_entry(data, "pypi", "pypi_version")
    github = _version_entry(data, "github_release", "github_version")
    commit_window = data.get("commit_window") if isinstance(data.get("commit_window"), dict) else {}

    lines: list[str] = []
    lines.append(f"# Daily Report - {date}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(summary)
    lines.append("")
    lines.append("## Pipeline Status")
    lines.append("")
    lines.append("| Step | Result | Duration | Notes |")
    lines.append("|------|--------|----------|-------|")
    for step in steps:
        name = str(step.get("name", "Unknown"))
        result = str(step.get("result", "unknown"))
        duration = _format_duration(step.get("duration"))
        notes = str(step.get("notes", "")).replace("|", "\\|")
        lines.append(f"| {name} | {result} | {duration} | {notes} |")
    lines.append("")
    lines.append("## Monitor")
    lines.append("")

    if changes_detected is True:
        lines.append("- **Changes detected**: yes")
    elif changes_detected is False:
        lines.append("- **Changes detected**: no")
    else:
        lines.append("- **Changes detected**: unknown")

    if change_items:
        for item in change_items:
            lines.append(f"- {item}")
    elif changes_detected is False:
        lines.append("- No upstream changes detected.")

    if pypi.get("current") or github.get("current"):
        lines.append(f"- PyPI version: `{pypi.get('current') or 'N/A'}`")
        if pypi.get("previous"):
            lines.append(f"- Previous PyPI version: `{pypi['previous']}`")
        lines.append(f"- GitHub release: `{github.get('current') or 'N/A'}`")
        if github.get("previous"):
            lines.append(f"- Previous GitHub release: `{github['previous']}`")

    if commit_window:
        lines.append(
            "- Commit window: "
            f"`{commit_window.get('local_start', 'N/A')}` to `{commit_window.get('local_end', 'N/A')}` "
            f"(queried as `{commit_window.get('since_utc', 'N/A')}` to `{commit_window.get('until_utc', 'N/A')}`)"
        )

    commit_count = _daily_commit_count(data)
    if commit_count:
        lines.append(f"- Daily commits captured: {commit_count}")
    collection_errors = data.get("errors")
    if isinstance(collection_errors, list) and collection_errors:
        lines.append(f"- **Collection errors: {len(collection_errors)}**")
    lines.append("")

    update_step = _find_step(steps, "update")
    if update_step:
        lines.append("## Update Agent")
        lines.append("")
        lines.append(f"- Result: `{update_step.get('result', 'unknown')}`")
        lines.append(f"- Duration: `{_format_duration(update_step.get('duration'))}`")
        if update_step.get("exit_code") is not None:
            lines.append(f"- Exit code: `{update_step['exit_code']}`")
        if update_step.get("notes"):
            lines.append(f"- Notes: {update_step['notes']}")
        if isinstance(verify_report, dict):
            verify_status = verify_report.get("status") or verify_report.get("result")
            if verify_status:
                lines.append(f"- Verification result: `{verify_status}`")
        lines.append("")

    research_step = _find_step(steps, "research")
    issue_count = _issue_count(data)
    if research_step or issue_count:
        lines.append("## Research")
        lines.append("")
        if research_step:
            lines.append(f"- Result: `{research_step.get('result', 'unknown')}`")
            lines.append(f"- Duration: `{_format_duration(research_step.get('duration'))}`")
            if research_step.get("notes"):
                lines.append(f"- Notes: {research_step['notes']}")
        if issue_count:
            lines.append(f"- Issues evaluated: {issue_count}")
        lines.append("")

    failures = [step for step in steps if step.get("result") == "failed"]
    collection_errors = data.get("errors") if isinstance(data.get("errors"), list) else []
    if failures or collection_errors:
        lines.append("## Errors")
        lines.append("")
        for failed in failures:
            step_name = str(failed.get("name", "Unknown"))
            lines.append(f"### {step_name}")
            if failed.get("exit_code") is not None:
                lines.append(f"- Exit code: `{failed['exit_code']}`")
            output = failed.get("last_output") or _read_related_log(step_name)
            lines.append("- Last output:")
            lines.append("```text")
            lines.append(_tail(str(output) if output else None, lines=18))
            lines.append("```")
            lines.append("")
        if collection_errors:
            lines.append("### Upstream collection")
            for error in collection_errors:
                lines.append(f"- {error}")
            lines.append("")

    lines.append("## Cost")
    lines.append("")
    lines.append("| Agent | Cost | Turns |")
    lines.append("|------|------|-------|")
    cost_rows, total_cost = _extract_cost_rows(cost_log)
    if cost_rows:
        for row in cost_rows:
            turns = row["turns"] if row["turns"] is not None else "N/A"
            lines.append(f"| {row['agent']} | {_money(row['cost'])} | {turns} |")
        lines.append(f"| **Total** | {_money(total_cost, strong=True)} | |")
    else:
        lines.append("| N/A | N/A | N/A |")
    lines.append("")

    capability_matrix = data.get("capability_matrix_markdown")
    capability_events = data.get("capability_events")
    if isinstance(capability_matrix, str) and capability_matrix.strip():
        lines.append("## Framework Capability Matrix")
        lines.append("")
        lines.append(capability_matrix.strip())
        if isinstance(capability_events, list):
            lines.append("")
            lines.append(f"- Release-note capability evidence evaluated this run: {len(capability_events)}")
        lines.append("")

    project_detail_reports = data.get("project_detail_reports")
    if isinstance(project_detail_reports, list) and project_detail_reports:
        lines.append("## Project Detail Reports")
        lines.append("")

    evolution_briefs = data.get("evolution_briefs")
    if isinstance(evolution_briefs, list) and evolution_briefs:
        lines.append("## Evolution Briefs")
        lines.append("")
        for brief_path in evolution_briefs:
            relative = str(brief_path)
            label = Path(relative).stem.replace("_", " ")
            lines.append(f"- [{label}]({relative})")
        lines.append("")
        for report_path in project_detail_reports:
            relative = str(report_path)
            label = Path(relative).stem.replace("_", " ")
            lines.append(f"- [{label}]({relative})")
        lines.append("")

    lines.append("## State")
    lines.append("")
    persisted_release = None
    persisted_pypi = None
    tracked_issues: list[str] = []
    last_run_date = None

    if isinstance(state_data, dict):
        persisted_release = state_data.get("github_release_version") or state_data.get("github_version")
        persisted_pypi = state_data.get("pypi_version")
        last_run_date = state_data.get("last_run_date")
        raw_issues = state_data.get("trackedIssues") or state_data.get("tracked_issues")
        if isinstance(raw_issues, list):
            tracked_issues = [str(item) for item in raw_issues]

    lines.append(f"- Persisted GitHub release: `{persisted_release or github.get('current') or 'N/A'}`")
    lines.append(f"- Persisted PyPI version: `{persisted_pypi or pypi.get('current') or 'N/A'}`")
    lines.append(f"- Last run date: `{last_run_date or data.get('date') or date}`")
    if tracked_issues:
        lines.append(f"- Tracked issues: {', '.join(tracked_issues)}")
        lines.append(f"- Total tracked issues: {len(tracked_issues)}")
    else:
        lines.append("- Tracked issues: N/A")

    if isinstance(pipeline_log, dict):
        lines.append("")
        lines.append("## Source Availability")
        lines.append("")
        lines.append("- Pipeline log: available")
        lines.append(f"- Change report: {'available' if change_report is not None else 'unavailable'}")
        lines.append(f"- Verify report: {'available' if verify_report is not None else 'unavailable'}")
        lines.append(f"- Cost log: {'available' if cost_log is not None else 'unavailable'}")

    report_text = "\n".join(lines).rstrip() + "\n"
    metadata = {"total_cost": total_cost}
    return report_text, summary, metadata


def _update_changelog(date: str, summary: str, report_relative_path: str) -> None:
    header = "# Changelog\n\n"
    existing = _read_text(CHANGELOG_PATH) or header
    if not existing.startswith("# Changelog"):
        existing = header + existing.lstrip()

    body = re.sub(rf"(?ms)^## {re.escape(date)}\n.*?(?=^## |\Z)", "", existing[len(header):]).lstrip()
    summary_line = summary.split(".")[0].strip().rstrip(".")
    entry = (
        f"## {date}\n\n"
        f"- {summary_line}\n"
        "- Daily monitor report generated and archived.\n"
        f"- [Full report]({report_relative_path})\n\n"
    )
    CHANGELOG_PATH.write_text(header + entry + body, encoding="utf-8")


def _update_readme_cost_log(
    date: str,
    release_version: str,
    update_cost: float | None,
    research_cost: float | None,
    report_cost: float | None,
    total_cost: float | None,
    notes: str,
) -> None:
    content = _read_text(README_PATH) or "# vLLM Version Monitor\n"

    marker = "_Last 7 days only._"
    table_header = (
        "| Date | Release | Update | Research | Report | Total | Notes |\n"
        "|------|---------|--------|----------|--------|-------|-------|\n"
    )
    new_row = (
        f"| {date} | {release_version} | {_money(update_cost, unavailable='—')} | {_money(research_cost, unavailable='—')} | "
        f"{_money(report_cost, unavailable='—')} | {_money(total_cost, strong=True, unavailable='—')} | {notes} |"
    )

    section_regex = re.compile(r"(?ms)^## Cost Log\n.*?(?=^## |\Z)")
    section_match = section_regex.search(content)

    existing_rows: list[str] = []
    if section_match:
        section = section_match.group(0)
        existing_rows = [
            line.strip()
            for line in section.splitlines()
            if line.strip().startswith("|")
            and "Date | Release" not in line
            and "Date | SDK Version" not in line
            and not line.strip().startswith("|------")
        ]

    filtered_rows = [row for row in existing_rows if not row.startswith(f"| {date} |")]
    filtered_rows.insert(0, new_row)
    filtered_rows = filtered_rows[:7]

    rendered_section = (
        "## Cost Log\n\n"
        + table_header
        + "\n".join(filtered_rows)
        + "\n\n"
        + marker
        + "\n"
    )

    if section_match:
        content = content[: section_match.start()] + rendered_section + content[section_match.end() :]
    else:
        if not content.endswith("\n"):
            content += "\n"
        content += "\n" + rendered_section

    README_PATH.write_text(content, encoding="utf-8")


def _build_sdk_user_message(payload: dict[str, Any], date: str) -> str:
    pipeline_log_path = Path(os.environ.get("PIPELINE_LOG", str(PIPELINE_LOG_PATH)))
    pipeline_log = _read_text(pipeline_log_path)
    change_report = _read_text(CHANGE_REPORT_PATH)
    verify_report = _read_text(VERIFY_REPORT_PATH)
    cost_log = _read_text(COST_LOG_PATH)
    state_json = _read_text(STATE_PATH) or "{}"

    message = f"""
You are working in the skill directory: {SKILL_ROOT}
Today's date is: {date}
Write the report to: {SKILL_ROOT / "reports" / f"{date}.md"}

## Available Data

### Pipeline Log ({pipeline_log_path}) — PRIMARY SOURCE
{f"```json\n{pipeline_log}\n```" if pipeline_log else "Not available — pipeline log was not created."}

### state.json
```json
{state_json}
```

### Monitor Payload (from monitor.py)
```json
{json.dumps(payload, ensure_ascii=False, indent=2)}
```
"""

    if change_report:
        message += f"""
### Change Report (/tmp/change-report.json)
```json
{change_report}
```
"""
    else:
        message += """
### Change Report
No change report found.
"""

    if verify_report:
        message += f"""
### Verify Report (/tmp/verify-report.json)
```json
{verify_report}
```
"""

    if cost_log:
        message += f"""
### Agent Costs (/tmp/agent-costs.json)
```json
{cost_log}
```
"""

    message += """
Please check `git log --oneline -5` and `git diff HEAD` for additional context.
Then write the daily report, prepend CHANGELOG entry, and update README Cost Log.
"""
    return message.strip()


def _message_type(message: Any) -> str | None:
    if isinstance(message, dict):
        value = message.get("type")
        return str(value) if value is not None else None
    value = getattr(message, "type", None)
    return str(value) if value is not None else None


def _message_attr(message: Any, key: str, default: Any = None) -> Any:
    if isinstance(message, dict):
        return message.get(key, default)
    return getattr(message, key, default)


def _build_sdk_options(system_prompt: str, clean_env: dict[str, str]) -> Any:
    from claude_agent_sdk import ClaudeAgentOptions

    # Keep option names aligned with Python SDK fields.
    options = {
        "system_prompt": system_prompt,
        "permission_mode": "bypassPermissions",
        "allowed_tools": ["Read", "Write", "Bash", "Glob", "Grep"],
        "setting_sources": [],
        "max_turns": 10,
        "max_budget_usd": 0.25,
        "cwd": str(SKILL_ROOT),
        "env": clean_env,
    }
    return ClaudeAgentOptions(**options)


def _write_report_cost(cost_usd: float, turns: int, date: str) -> None:
    try:
        existing = _read_json(COST_LOG_PATH)
        if not isinstance(existing, dict):
            existing = {}
        existing["report"] = {"costUsd": cost_usd, "turns": turns, "date": date}
        COST_LOG_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        # Cost logging is non-critical.
        return


def _validate_report_artifacts(report_path: Path, date: str) -> None:
    errors: list[str] = []
    report_text = _read_text(report_path)
    if not report_text or f"# Daily Report - {date}" not in report_text:
        errors.append("daily report missing expected heading")

    changelog_text = _read_text(CHANGELOG_PATH)
    if not changelog_text or f"## {date}" not in changelog_text or f"[Full report](reports/{date}.md)" not in changelog_text:
        errors.append("CHANGELOG.md missing today's entry")

    readme_text = _read_text(README_PATH)
    if not readme_text or "## Cost Log" not in readme_text or f"| {date} |" not in readme_text:
        errors.append("README.md missing today's cost row")

    if errors:
        raise RuntimeError("; ".join(errors))


async def _generate_report_with_sdk(payload: dict[str, Any]) -> str:
    from claude_agent_sdk import query

    date = _today()
    report_path = REPORTS_DIR / f"{date}.md"
    system_prompt = _read_required_text(SYSTEM_PROMPT_PATH, "system prompt")
    user_message = _build_sdk_user_message(payload, date)

    clean_env = dict(os.environ)
    clean_env.pop("CLAUDECODE", None)
    options = _build_sdk_options(system_prompt=system_prompt, clean_env=clean_env)

    print("Report Agent (Python SDK) starting ...")
    print(f"  Skill root: {SKILL_ROOT}")
    print(f"  Report path: reports/{date}.md")

    turns = 0
    result_message: Any = None

    stream = query(prompt=user_message, options=options)
    async for message in stream:
        msg_type = _message_type(message)
        if msg_type == "assistant":
            turns += 1
        elif msg_type == "result":
            result_message = message

    report_cost = _message_attr(result_message, "total_cost_usd", 0.0) if result_message else 0.0
    report_cost = _safe_float(report_cost) or 0.0
    _write_report_cost(cost_usd=report_cost, turns=turns, date=date)

    if report_path.exists():
        _validate_report_artifacts(report_path, date)
        print("Report agent finished.")
        print(f"  Cost: ${report_cost:.4f}")
        print(f"  Turns: {turns}")
        print(f"  Report written: reports/{date}.md")
        print("Report complete.")
        return str(report_path)

    raise RuntimeError("Report file was not created by Claude Agent SDK run.")


def _generate_report_fallback(data: dict[str, Any] | None = None) -> str:
    payload = data or {}
    date = _today()

    pipeline_log_path = Path(os.environ.get("PIPELINE_LOG", str(PIPELINE_LOG_PATH)))
    pipeline_log = _read_json(pipeline_log_path)
    change_report = _read_json(CHANGE_REPORT_PATH)
    verify_report = _read_json(VERIFY_REPORT_PATH)
    cost_log = _read_json(COST_LOG_PATH)
    state_data = _read_json(STATE_PATH)

    report_content, summary, metadata = _build_report(
        date=date,
        data=payload,
        pipeline_log=pipeline_log,
        change_report=change_report,
        verify_report=verify_report,
        cost_log=cost_log,
        state_data=state_data,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{date}.md"
    report_path.write_text(report_content, encoding="utf-8")

    _update_changelog(date, summary, f"reports/{date}.md")

    cost_rows, fallback_total = _extract_cost_rows(cost_log)
    per_agent: dict[str, float] = {}
    for row in cost_rows:
        lower_name = str(row.get("agent", "")).lower()
        cost = row.get("cost")
        if isinstance(cost, float):
            per_agent[lower_name] = per_agent.get(lower_name, 0.0) + cost

    update_cost = sum(value for key, value in per_agent.items() if "update" in key) or None
    research_cost = sum(value for key, value in per_agent.items() if "research" in key) or None
    report_cost = sum(value for key, value in per_agent.items() if "report" in key) or None
    total_cost = metadata.get("total_cost") if isinstance(metadata.get("total_cost"), float) else fallback_total

    notes = summary.split(".")[0].strip()
    pypi = _version_entry(payload, "pypi", "pypi_version")
    github = _version_entry(payload, "github_release", "github_version")
    release_version = str(github.get("current") or pypi.get("current") or "N/A")
    _update_readme_cost_log(
        date=date,
        release_version=release_version,
        update_cost=update_cost,
        research_cost=research_cost,
        report_cost=report_cost,
        total_cost=total_cost,
        notes=notes,
    )

    git_log = _run_git("log", "--oneline", "-5")
    git_diff = _run_git("diff", "HEAD")
    if git_log:
        print("Recent commits:")
        print(git_log)
    if git_diff:
        print("Detected uncommitted diff while generating report.")

    print(f"Report generated: {report_path}")
    return str(report_path)


def generate_report(data: dict[str, Any] | None = None) -> str:
    payload = data or {}

    try:
        return asyncio.run(_generate_report_with_sdk(payload))
    except ModuleNotFoundError as exc:
        print(f"Claude Agent SDK unavailable, fallback enabled: {exc}")
    except Exception as exc:
        print(f"Claude Agent SDK run failed, fallback enabled: {exc}")

    return _generate_report_fallback(payload)


if __name__ == "__main__":
    generate_report({})
