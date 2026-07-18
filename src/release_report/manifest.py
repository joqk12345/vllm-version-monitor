from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import validate

from .config import Config


def _artifact(path: Path, root: Path) -> dict:
    return {"path": str(path.relative_to(root)), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def write_manifest(root: Path, config: Config, cutoff: str, source_mode: str, latest_stable: str, files: list[Path]) -> Path:
    path = root / "build_manifest.json"
    payload = {"schema_version": 1, "project": config.repo_slug, "cutoff": cutoff, "source_mode": source_mode, "latest_stable": latest_stable, "artifacts": [_artifact(file, root) for file in files]}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def validate_manifest(root: Path, schema_root: Path) -> dict:
    path = root / "build_manifest.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads((schema_root / "build_manifest.schema.json").read_text(encoding="utf-8"))
    validate(payload, schema)
    for artifact in payload["artifacts"]:
        target = root / artifact["path"]
        if not target.exists() or target.stat().st_size != artifact["bytes"] or hashlib.sha256(target.read_bytes()).hexdigest() != artifact["sha256"]:
            raise ValueError(f"Manifest artifact mismatch: {target}")
    return payload


def validate_verification(path: Path, schema_root: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads((schema_root / "verification.schema.json").read_text(encoding="utf-8"))
    validate(payload, schema)
    return payload
