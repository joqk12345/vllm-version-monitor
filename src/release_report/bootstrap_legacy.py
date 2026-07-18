"""One-time importer for prior official GitHub-release cache collected by this repository."""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--database", default="data/monitor.db")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    with sqlite3.connect(args.database) as conn:
        rows = conn.execute("SELECT raw_payload_json FROM project_snapshots WHERE project_id = ? ORDER BY run_id DESC", (args.project,)).fetchall()
    for row in rows:
        payload = json.loads(row[0])
        catalog = payload.get("release_catalog") if isinstance(payload, dict) else None
        if isinstance(catalog, list) and catalog:
            output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps({"metadata": {"source_url": f"https://api.github.com/repos/{payload['github_repo']}/releases", "retrieved_at": datetime.now(timezone.utc).isoformat(), "import_note": "Migrated from earlier official GitHub API collection."}, "releases": catalog, "source_mode": "cache_migrated_official"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return 0
    raise SystemExit(f"No cached release catalog found for {args.project}")


if __name__ == "__main__":
    raise SystemExit(main())
