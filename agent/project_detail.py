from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from capabilities import Capability, extract_capability_events


def _release_date(release: dict[str, Any]) -> str:
    published_at = str(release.get("published_at") or "")
    return published_at[:10] if published_at else "—"


def _series(tag: str) -> str:
    match = re.search(r"v?(\d+\.\d+)", tag)
    return f"{match.group(1)}.x" if match else "其他版本"


def _link(tag: str, url: str | None) -> str:
    return f"[{tag}]({url})" if url else tag


def _compact_evidence(events: list[dict[str, Any]]) -> str:
    if not events:
        return "Release notes 未匹配到已配置能力关键词"
    snippets: list[str] = []
    for event in events[:3]:
        text = str(event["evidence_text"]).replace("|", "\\|")
        snippets.append(text[:150] + ("…" if len(text) > 150 else ""))
    return "<br>".join(snippets)


def render_project_detail(
    project: dict[str, Any], releases: list[dict[str, Any]], capabilities: list[Capability]
) -> str:
    """Render a project-specific release evolution report from source evidence."""
    release_events: dict[str, list[dict[str, Any]]] = {}
    all_events: list[dict[str, Any]] = []
    chronological_releases = sorted(releases, key=lambda item: str(item.get("published_at") or ""))
    for release in chronological_releases:
        release_project = {
            "id": project["id"],
            "name": project["name"],
            "versions": {"github_release": {"current": release.get("tag_name"), "html_url": release.get("html_url")}},
            "latest_release_notes": release.get("body") or "",
        }
        events = extract_capability_events(release_project, capabilities)
        release_events[str(release.get("tag_name"))] = events
        all_events.extend(events)

    current = project.get("versions", {}).get("github_release", {})
    pypi = project.get("versions", {}).get("pypi", {})
    lines = [f"# {project['name']} 版本与 Feature 明细", ""]
    lines.extend([
        "## 当前状态", "",
        f"- GitHub Release：{_link(str(current.get('current') or '—'), current.get('html_url'))}",
        f"- 发布时间：{str(current.get('published_at') or '—')}",
        f"- PyPI：`{pypi.get('current') or '—'}`",
        f"- 历史 Releases：{len(releases)} 条（仅含 GitHub 正式 Release，draft 已排除）",
        "",
        "## 版本演进总览", "",
        "以下按 GitHub Release 的 `major.minor` 分组。Feature 描述保留 release note 原文，便于回溯验证。", "",
    ])
    collection_errors = project.get("errors")
    if isinstance(collection_errors, list) and collection_errors:
        lines.extend(["## 数据采集状态", "", "- 本次采集存在错误，以下明细可能不完整："])
        lines.extend(f"- {error}" for error in collection_errors)
        lines.append("")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for release in chronological_releases:
        grouped.setdefault(_series(str(release.get("tag_name") or "")), []).append(release)
    for series, items in grouped.items():
        lines.extend([f"### {series}", "", "| 版本 | 日期 | 关键 Feature / 修复证据 |", "|---|---:|---|"])
        for release in items:
            tag = str(release.get("tag_name") or "—")
            lines.append(f"| {_link(tag, release.get('html_url'))} | {_release_date(release)} | {_compact_evidence(release_events[tag])} |")
        lines.append("")
    if not grouped:
        lines.extend(["- 本次未获得 Release 历史；请先处理上述数据源错误后再运行。", ""])

    lines.extend(["## 关键 Feature 的首次与最近证据", "", "| 能力 | 首次证据 | 最近证据 |", "|---|---|---|"])
    for capability in capabilities:
        events = [event for event in all_events if event["capability_id"] == capability.id]
        if not events:
            lines.append(f"| {capability.name} | — | — |")
            continue
        first, latest = events[0], events[-1]
        first_text = f"{first['release_tag']}：{first['evidence_text'][:90]}"
        latest_text = f"{latest['release_tag']}：{latest['evidence_text'][:90]}"
        escaped_first = first_text.replace("|", "\\|")
        escaped_latest = latest_text.replace("|", "\\|")
        lines.append(f"| {capability.name} | {escaped_first} | {escaped_latest} |")

    observed = [capability.name for capability in capabilities if any(event["capability_id"] == capability.id for event in all_events)]
    lines.extend(["", "## 自动化观察", ""])
    if observed:
        lines.append(f"- 在已采集的 release note 中，`{project['name']}` 有直接证据覆盖：{', '.join(observed)}。")
        lines.append("- 此报告描述的是 Release 明确披露的能力演进；未出现的能力应视为“尚未采集到证据”，而不是“不支持”。")
    else:
        lines.append("- 当前 release note 未命中能力词典；请扩展 `config/capabilities.json` 的关键词，或补充人工注释。")
    lines.append("")
    return "\n".join(lines)


def write_project_detail(path: Path, project: dict[str, Any], releases: list[dict[str, Any]], capabilities: list[Capability]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_project_detail(project, releases, capabilities), encoding="utf-8")
    return path
