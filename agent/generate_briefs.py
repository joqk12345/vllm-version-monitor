from __future__ import annotations

from datetime import datetime
from pathlib import Path

from capabilities import load_capabilities
from evolution_brief import write_evolution_brief
from projects import load_projects
from storage import MonitorStore

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parent


def main() -> None:
    capabilities = load_capabilities(ROOT / "config" / "capabilities.json")
    store = MonitorStore(ROOT / "data" / "monitor.db")
    date = datetime.now().date().isoformat()
    written = 0
    for config in load_projects(ROOT / "config" / "projects.json"):
        payload = store.latest_project_payload(config.id)
        if payload is None:
            print(f"No release history available for {config.name}; run monitor.py first.")
            continue
        path = write_evolution_brief(ROOT / "reports" / "briefs" / f"{config.id}.md", payload, payload["release_catalog"], capabilities, date)
        print(f"Wrote {path.relative_to(ROOT)}")
        written += 1
    if not written:
        raise SystemExit("No briefs generated.")


if __name__ == "__main__":
    main()
