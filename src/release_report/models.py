from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ReleaseRecord:
    tag: str
    normalized_version: str
    series: str
    published_at: str
    created_at: str | None
    is_draft: bool
    is_prerelease: bool
    release_kind: str
    release_url: str
    body_markdown: str
    body_text: str
    source_retrieved_at: str
    source_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeatureEvidence:
    tag: str
    category: str
    snippet: str
    source_url: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class Stage:
    name: str
    summary: str
    releases: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "summary": self.summary, "releases": list(self.releases)}
