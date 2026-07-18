from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Capability:
    id: str
    name: str
    keywords: tuple[str, ...]


def load_capabilities(path: Path) -> list[Capability]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load capability config {path}: {exc}") from exc
    entries = raw.get("capabilities") if isinstance(raw, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError("Capability config must contain a non-empty 'capabilities' list")
    capabilities: list[Capability] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Each capability definition must be an object")
        identifier = str(entry.get("id") or "").strip()
        name = str(entry.get("name") or "").strip()
        keywords = entry.get("keywords")
        if not identifier or not name or not isinstance(keywords, list) or not keywords:
            raise ValueError("Capability definitions require id, name, and keywords")
        capabilities.append(Capability(identifier, name, tuple(str(keyword).lower() for keyword in keywords)))
    return capabilities


def _release_items(release_notes: str) -> list[str]:
    """Extract concise, human-reviewable release-note items without rewriting them."""
    items: list[str] = []
    for line in release_notes.splitlines():
        text = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", line).strip()
        if len(text) >= 12 and not text.startswith("#"):
            items.append(text)
    return items


def _status(text: str) -> str:
    value = text.lower()
    if any(word in value for word in ("deprecat", "removed", "drop support")):
        return "deprecated"
    if any(word in value for word in ("experimental", "preview", "beta", "prototype")):
        return "experimental"
    if any(word in value for word in ("fix", "bug", "regression")):
        return "fixed"
    return "supported"


def _evidence_score(text: str, matched_keywords: list[str]) -> int:
    """Prefer feature statements over changelog noise such as individual PR fixes."""
    value = text.lower()
    score = len(matched_keywords) * 10
    for phrase, weight in (
        ("new feature", 30), ("introduc", 24), ("support", 20), ("enable", 20),
        ("add ", 18), ("improv", 12), ("optim", 12), ("performance", 12),
        ("fix", 4),
    ):
        if phrase in value:
            score += weight
    return score


def _matches_keyword(text: str, keyword: str) -> bool:
    """Match a capability term as a term, not as an accidental substring."""
    return re.search(rf"(?<![a-z0-9]){re.escape(keyword.lower())}(?![a-z0-9])", text.lower()) is not None


def extract_capability_events(
    project: dict[str, Any], capabilities: list[Capability]
) -> list[dict[str, Any]]:
    """Classify release-note evidence using explicit keyword matches.

    This intentionally emits the original release-note line as evidence rather
    than converting it into an untraceable generated claim.
    """
    notes = project.get("latest_release_notes")
    release = project.get("versions", {}).get("github_release", {})
    release_tag = release.get("current") if isinstance(release, dict) else None
    release_url = release.get("html_url") if isinstance(release, dict) else None
    if not isinstance(notes, str) or not notes.strip() or not release_tag:
        return []

    best_matches: dict[str, tuple[int, str, list[str]]] = {}
    for item in _release_items(notes):
        lower_item = item.lower()
        for capability in capabilities:
            matched = [keyword for keyword in capability.keywords if _matches_keyword(lower_item, keyword)]
            if not matched:
                continue
            candidate = (_evidence_score(item, matched), item, matched)
            existing = best_matches.get(capability.id)
            if existing is None or candidate[0] > existing[0]:
                best_matches[capability.id] = candidate

    events: list[dict[str, Any]] = []
    for capability in capabilities:
        match = best_matches.get(capability.id)
        if match is None:
            continue
        score, item, matched = match
        events.append({
            "project_id": project["id"], "project_name": project["name"],
            "capability_id": capability.id, "capability_name": capability.name,
            "release_tag": release_tag, "status": _status(item), "evidence_text": item,
            "evidence_url": release_url, "matched_keywords": matched,
            "confidence": "high" if len(matched) > 1 else "medium", "relevance_score": score,
        })
    return events


def render_capability_matrix(
    projects: list[dict[str, Any]], capabilities: list[Capability], matrix: dict[tuple[str, str], dict[str, Any]]
) -> str:
    """Render a compact latest-known capability matrix for Markdown reports."""
    lines = [
        "| 能力 | " + " | ".join(project["name"] for project in projects) + " |",
        "|---|" + "|".join("---" for _ in projects) + "|",
    ]
    for capability in capabilities:
        cells: list[str] = []
        for project in projects:
            event = matrix.get((project["id"], capability.id))
            if not event:
                cells.append("—")
                continue
            tag = event.get("release_tag") or "?"
            status = event.get("status") or "supported"
            cells.append(f"{status} ({tag})")
        lines.append(f"| {capability.name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)
