from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

from .classify import classify
from .config import load_config
from .fetch import fetch_releases
from .normalize import normalize_releases, write_normalized
from .render_brief import render_brief
from .render_detail import render_detail
from .stages import build_stages
from .verify import verify_pdfs
from .manifest import validate_manifest, validate_verification, write_manifest


def _paths(config, run_id: str | None = None):
    root = config.path.parent.parent
    output_root = root / config.project["output"].get("directory", "output")
    if run_id:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id):
            raise ValueError("run_id may contain only letters, digits, dot, underscore, and hyphen")
        output_root = output_root / "runs" / run_id
    return output_root, output_root / "json", output_root / "pdf", output_root / "qa"


def analyze(config, cutoff, offline, run_id=None):
    raw = fetch_releases(config, offline=offline)
    records = normalize_releases(raw, config, cutoff)
    if not records: raise RuntimeError("No releases remain after normalization/cutoff")
    _, json_dir, _, _ = _paths(config, run_id)
    slug = config.project["repository"].replace("-", "_")
    write_normalized(records, json_dir / f"{slug}_releases_normalized.json")
    features = classify(records, config); stages = build_stages(records, config)
    (json_dir / f"{slug}_milestones.json").write_text(json.dumps({"stages": [stage.to_dict() for stage in stages], "features": [feature.to_dict() for feature in features]}, indent=2) + "\n", encoding="utf-8")
    return records, features, stages


def run(args):
    config = load_config(args.config); cutoff = args.cutoff or str(config.project.get("cutoff")); offline = bool(getattr(args, "offline", False))
    run_id = getattr(args, "run_id", None)
    if args.command == "fetch": fetch_releases(config, offline); return 0
    if args.command == "verify":
        output_root, _, pdf_dir, qa_dir = _paths(config, run_id)
        normalized = json.loads((output_root / "json" / f"{config.project['repository'].replace('-', '_')}_releases_normalized.json").read_text(encoding="utf-8"))
        stable = [item for item in normalized if item["release_kind"] == "stable"]
        if not stable: raise RuntimeError("No stable releases in normalized output")
        latest = stable[-1]["tag"]
        verify_pdfs(pdf_dir, qa_dir, config.project["output"]["detailed_pdf"], config.project["output"]["brief_pdf"], latest, config.project["titles"]["brief"])
        validate_manifest(output_root, config.path.parent.parent / "schemas")
        validate_verification(qa_dir / "verification.json", config.path.parent.parent / "schemas")
        return 0
    records, features, stages = analyze(config, cutoff, offline, run_id)
    if args.command == "analyze": return 0
    output_root, json_dir, pdf_dir, qa_dir = _paths(config, run_id); pdf_dir.mkdir(parents=True, exist_ok=True)
    render_detail(pdf_dir / config.project["output"]["detailed_pdf"], config, records, features, stages, cutoff)
    render_brief(pdf_dir / config.project["output"]["brief_pdf"], config, records, features, stages, cutoff)
    latest = [record for record in records if record.release_kind == "stable"][-1]
    manifest = write_manifest(output_root, config, cutoff, latest.source_mode, latest.tag, [json_dir / f"{config.project['repository'].replace('-', '_')}_releases_normalized.json", json_dir / f"{config.project['repository'].replace('-', '_')}_milestones.json", pdf_dir / config.project["output"]["detailed_pdf"], pdf_dir / config.project["output"]["brief_pdf"]])
    if args.command == "render": return 0
    verify_pdfs(pdf_dir, qa_dir, config.project["output"]["detailed_pdf"], config.project["output"]["brief_pdf"], latest.tag, config.project["titles"]["brief"])
    validate_manifest(output_root, config.path.parent.parent / "schemas")
    validate_verification(qa_dir / "verification.json", config.path.parent.parent / "schemas")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="release-report")
    parser.add_argument("command", choices=["fetch", "analyze", "render", "verify", "build"])
    parser.add_argument("--config", required=True); parser.add_argument("--cutoff"); parser.add_argument("--offline", action="store_true")
    parser.add_argument("--run-id", help="Write artifacts under output/<project>/runs/<run-id>.")
    args = parser.parse_args(argv)
    try: return run(args)
    except Exception as exc:
        logging.error("release-report failed: %s", exc); return 1


if __name__ == "__main__":
    raise SystemExit(main())
