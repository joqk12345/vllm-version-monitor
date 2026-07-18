from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from packaging.version import InvalidVersion, Version

from .config import Config
from .models import ReleaseRecord


def version_from_tag(tag: str) -> Version | None:
    try:
        return Version(tag.lstrip("v"))
    except InvalidVersion:
        return None


def normalize_releases(raw: dict[str, Any], config: Config, cutoff: str | None = None) -> list[ReleaseRecord]:
    cutoff_date = date.fromisoformat(cutoff or str(config.project.get("cutoff"))) if (cutoff or config.project.get("cutoff")) else None
    retrieved = str(raw.get("metadata", {}).get("retrieved_at") or datetime.now(timezone.utc).isoformat())
    mode = str(raw.get("source_mode") or "unknown")
    records: list[ReleaseRecord] = []
    for item in raw.get("releases", []):
        if not isinstance(item, dict) or item.get("draft"):
            continue
        tag = str(item.get("tag_name") or "")
        version = version_from_tag(tag)
        if not tag or version is None:
            continue
        published = str(item.get("published_at") or "")
        if not published:
            continue
        if cutoff_date and date.fromisoformat(published[:10]) > cutoff_date:
            continue
        prerelease = bool(item.get("prerelease")) or bool(re.search(config.data["release_rules"]["rc_pattern"], tag, re.I))
        if prerelease:
            kind = "rc"
        elif re.search(config.data["release_rules"]["post_pattern"], tag, re.I):
            kind = "post"
        elif re.search(config.data["release_rules"]["patch_pattern"], tag, re.I):
            kind = "patch"
        else:
            kind = "stable"
        body = str(item.get("body") or "")
        text = re.sub(r"`|[*_#]", "", body)
        records.append(ReleaseRecord(tag, str(version), f"{version.major}.{version.minor}.x", published, item.get("created_at"), False, prerelease, kind, str(item.get("html_url") or ""), body, text, retrieved, mode))
    by_tag: dict[str, ReleaseRecord] = {record.tag: record for record in records}
    return sorted(by_tag.values(), key=lambda record: (version_from_tag(record.tag) or Version("0"), record.published_at))


def write_normalized(records: list[ReleaseRecord], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([record.to_dict() for record in records], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
