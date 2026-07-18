from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Config:
    path: Path
    data: dict[str, Any]

    @property
    def project(self) -> dict[str, Any]:
        return self.data["project"]

    @property
    def repo_slug(self) -> str:
        return f"{self.project['owner']}/{self.project['repository']}"


def load_config(path: str | Path) -> Config:
    resolved = Path(path).resolve()
    raw = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("project"), dict):
        raise ValueError("Config requires a project section")
    for key in ("owner", "repository", "display_name", "titles", "output"):
        if key not in raw["project"]:
            raise ValueError(f"Missing project.{key}")
    return Config(resolved, raw)
