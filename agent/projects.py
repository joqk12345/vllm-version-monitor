from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """A monitored upstream project and its version sources."""

    id: str
    name: str
    github_repo: str
    pypi_package: str | None = None


def load_projects(config_path: Path) -> list[ProjectConfig]:
    """Load and validate project definitions from the repository config."""
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load project config {config_path}: {exc}") from exc

    entries = raw.get("projects") if isinstance(raw, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError("Project config must contain a non-empty 'projects' list")

    projects: list[ProjectConfig] = []
    seen_ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Each project definition must be an object")
        project_id = str(entry.get("id") or "").strip()
        name = str(entry.get("name") or "").strip()
        github_repo = str(entry.get("github_repo") or "").strip()
        pypi_package = entry.get("pypi_package")
        if not project_id or not name or not github_repo:
            raise ValueError("Project definitions require id, name, and github_repo")
        if project_id in seen_ids:
            raise ValueError(f"Duplicate project id: {project_id}")
        seen_ids.add(project_id)
        projects.append(
            ProjectConfig(
                id=project_id,
                name=name,
                github_repo=github_repo,
                pypi_package=str(pypi_package).strip() if pypi_package else None,
            )
        )
    return projects
