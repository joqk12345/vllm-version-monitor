from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from capabilities import Capability, extract_capability_events


def _date(value: Any) -> str:
    return str(value or "—")[:10]


def _series(tag: str) -> str:
    match = re.search(r"v?(\d+\.\d+)", tag)
    return f"{match.group(1)}.x" if match else "其他"


def _link(tag: str, url: str | None) -> str:
    return f"[{tag}]({url})" if url else tag


def _events_for_release(project: dict[str, Any], release: dict[str, Any], capabilities: list[Capability]) -> list[dict[str, Any]]:
    return extract_capability_events(
        {
            "id": project["id"], "name": project["name"],
            "versions": {"github_release": {"current": release.get("tag_name"), "html_url": release.get("html_url")}},
            "latest_release_notes": release.get("body") or "",
        },
        capabilities,
    )


def _phase_groups(releases: list[dict[str, Any]], max_phases: int = 5) -> list[list[dict[str, Any]]]:
    by_series: list[list[dict[str, Any]]] = []
    for release in releases:
        series = _series(str(release.get("tag_name") or ""))
        if not by_series or _series(str(by_series[-1][-1].get("tag_name") or "")) != series:
            by_series.append([])
        by_series[-1].append(release)
    if len(by_series) <= max_phases:
        return by_series
    # Keep chronological order while collapsing many version lines into five editorial phases.
    size = (len(by_series) + max_phases - 1) // max_phases
    return [[release for group in by_series[index:index + size] for release in group] for index in range(0, len(by_series), size)]


def _theme(events: list[dict[str, Any]]) -> str:
    names = [event["capability_name"] for event in events]
    common = [name for name, _ in Counter(names).most_common(3)]
    return "、".join(common) if common else "Release notes 未命中当前能力词典（待复核）"


def _milestones(releases: list[dict[str, Any]], events_by_tag: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    candidates = [release for release in releases if events_by_tag.get(str(release.get("tag_name")))]
    if not candidates:
        return releases[-1:] if releases else []

    def score(release: dict[str, Any]) -> int:
        events = events_by_tag[str(release.get("tag_name"))]
        relevance = sum(int(event.get("relevance_score", 0)) for event in events)
        non_fix = sum(event.get("status") != "fixed" for event in events)
        return relevance + non_fix * 15 + len(events) * 5

    selected: dict[str, dict[str, Any]] = {}
    # Anchor the narrative with the first and latest documented capability releases.
    selected[str(candidates[0].get("tag_name"))] = candidates[0]
    selected[str(candidates[-1].get("tag_name"))] = candidates[-1]
    # Preserve one strong architectural inflection point from each timeline phase.
    for phase in _phase_groups(candidates):
        winner = max(phase, key=score)
        selected[str(winner.get("tag_name"))] = winner
    for release in sorted(candidates, key=score, reverse=True):
        if len(selected) >= min(12, len(candidates)):
            break
        selected[str(release.get("tag_name"))] = release
    return sorted(selected.values(), key=lambda item: str(item.get("published_at") or ""))


def render_evolution_brief(project: dict[str, Any], releases: list[dict[str, Any]], capabilities: list[Capability], as_of: str) -> str:
    """Render the two-page editorial brief layout from official release evidence."""
    releases = sorted(releases, key=lambda item: str(item.get("published_at") or ""))
    events_by_tag = {str(release.get("tag_name")): _events_for_release(project, release, capabilities) for release in releases}
    all_events = [event for release_events in events_by_tag.values() for event in release_events]
    current = project.get("versions", {}).get("github_release", {})
    stable_releases = [release for release in releases if ".post" not in str(release.get("tag_name") or "")]
    stable = stable_releases[-1] if stable_releases else (releases[-1] if releases else {})
    patch = releases[-1] if releases and ".post" in str(releases[-1].get("tag_name") or "") else None

    lines = ["# TECHNOLOGY BRIEF / " + as_of[:7].replace("-", "."), "", f"# {project['name']} 版本演进简报", ""]
    lines.append("> 基于官方 GitHub Releases 的版本、Feature 与技术路线归纳。")
    lines.extend(["", f"**一句话结论**：{project['name']} 的版本演进以 {_theme(all_events)} 为主要证据主线；结论仅覆盖官方 Release 明确披露的能力。", ""])
    lines.append(f"**最新正式版本**：{_link(str(stable.get('tag_name') or '—'), stable.get('html_url'))}（{_date(stable.get('published_at'))}）。")
    if patch:
        lines.append(f"**最新稳定补丁**：{_link(str(patch.get('tag_name') or '—'), patch.get('html_url'))}（{_date(patch.get('published_at'))}）。")
    else:
        lines.append("**最新稳定补丁**：当前 Release 列表未单独识别到 post/patch 发布。")
    lines.extend(["", "## 01 版本演进时间线", "", "| 阶段 | 时间 | 代表版本 | 核心主题 |", "|---|---|---|---|"])
    phases = _phase_groups(releases)
    for number, group in enumerate(phases, 1):
        events = [event for release in group for event in events_by_tag[str(release.get("tag_name"))]]
        first, last = group[0], group[-1]
        versions = str(first.get("tag_name")) if first is last else f"{first.get('tag_name')}–{last.get('tag_name')}"
        lines.append(f"| 阶段 {number}：{_series(str(first.get('tag_name') or ''))} | {_date(first.get('published_at'))}–{_date(last.get('published_at'))} | {versions} | {_theme(events)} |")
    lines.extend(["", "## 02 核心判断", "", "| 技术主线 | 证据路径 |", "|---|---|"])
    tracks = [("性能与缓存", {"performance", "quantization"}), ("调度、并行与集群", {"scheduling_parallelism"}), ("模型、架构与服务接口", {"model_support", "serving_api", "hardware_backends"})]
    for label, ids in tracks:
        track_events = [event for event in all_events if event["capability_id"] in ids]
        if track_events:
            lines.append(f"| {label} | {track_events[0]['release_tag']} → {track_events[-1]['release_tag']}；{_theme(track_events)} |")
        else:
            lines.append(f"| {label} | 当前 Release 证据不足，待复核 |")
    lines.extend(["", "## 03 关键版本里程碑", "", "| 时间 | 版本 | 版本意义 / 关键 Feature |", "|---:|---|---|"])
    for release in _milestones(releases, events_by_tag):
        tag = str(release.get("tag_name") or "—")
        events = events_by_tag[tag]
        best_event = max(events, key=lambda event: int(event.get("relevance_score", 0))) if events else None
        evidence = str(best_event["evidence_text"]) if best_event else str(release.get("name") or "Release notes 待复核")
        lines.append(f"| {_date(release.get('published_at'))} | {_link(tag, release.get('html_url'))} | {evidence[:180].replace('|', '\\|')} |")
    lines.extend(["", "## 04 技术选型启示", ""])
    observed = _theme(all_events)
    lines.append(f"- **适合重点评估的场景**：需要 {observed} 相关能力，且接受较快版本节奏的部署环境。")
    lines.append("- **生产部署注意**：固定镜像、依赖与 Kernel 组合；将 stable、post/patch 与 rc/prerelease 分开验证。")
    lines.append("- **比较边界**：本简报说明官方披露的演进证据，不构成跨框架性能排名或兼容性承诺。")
    lines.extend(["", "## 05 版本与证据说明", "", f"- **资料来源**：[官方 GitHub Releases](https://github.com/{project['github_repo']}/releases)", f"- **截止日期**：{as_of}；发布日期按 UTC 统计。", "- **版本筛选**：仅纳入非 draft、非 prerelease 且 tag 以 `v` 开头的主项目 Release。", "- **证据边界**：未命中能力词典时标记为待复核，不等同于不支持。", ""])
    return "\n".join(lines)


def write_evolution_brief(path: Path, project: dict[str, Any], releases: list[dict[str, Any]], capabilities: list[Capability], as_of: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_evolution_brief(project, releases, capabilities, as_of), encoding="utf-8")
    return path
