from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS monitor_runs (
    id INTEGER PRIMARY KEY,
    collected_at TEXT NOT NULL,
    timezone TEXT NOT NULL,
    commit_window_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS project_snapshots (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES monitor_runs(id),
    project_id TEXT NOT NULL,
    project_name TEXT NOT NULL,
    pypi_version TEXT,
    github_release_version TEXT,
    github_release_published_at TEXT,
    github_release_url TEXT,
    commit_count INTEGER NOT NULL DEFAULT 0,
    issue_count INTEGER NOT NULL DEFAULT 0,
    raw_payload_json TEXT NOT NULL,
    UNIQUE(run_id, project_id)
);

CREATE INDEX IF NOT EXISTS project_snapshots_project_run
    ON project_snapshots(project_id, run_id DESC);

CREATE TABLE IF NOT EXISTS capability_events (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES monitor_runs(id),
    project_id TEXT NOT NULL,
    project_name TEXT NOT NULL,
    capability_id TEXT NOT NULL,
    capability_name TEXT NOT NULL,
    release_tag TEXT NOT NULL,
    release_published_at TEXT,
    status TEXT NOT NULL,
    evidence_text TEXT NOT NULL,
    evidence_url TEXT,
    matched_keywords_json TEXT NOT NULL,
    confidence TEXT NOT NULL,
    UNIQUE(project_id, capability_id, release_tag, evidence_text)
);

CREATE INDEX IF NOT EXISTS capability_events_latest
    ON capability_events(project_id, capability_id, id DESC);
"""


class MonitorStore:
    """Append-only history store; state.json remains only a lightweight cursor."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as conn:
            conn.executescript(SCHEMA)
            columns = {row[1] for row in conn.execute("PRAGMA table_info(capability_events)")}
            if "release_published_at" not in columns:
                conn.execute("ALTER TABLE capability_events ADD COLUMN release_published_at TEXT")

    def latest_versions(self, project_id: str) -> dict[str, str | None]:
        self.initialize()
        with sqlite3.connect(self.path) as conn:
            row = conn.execute(
                """
                SELECT pypi_version, github_release_version
                FROM project_snapshots
                WHERE project_id = ?
                ORDER BY run_id DESC
                LIMIT 1
                """,
                (project_id,),
            ).fetchone()
        if row is None:
            return {"pypi_version": None, "github_release_version": None}
        return {"pypi_version": row[0], "github_release_version": row[1]}

    def save_run(
        self,
        *,
        collected_at: str,
        timezone: str,
        commit_window: dict[str, str],
        projects: list[dict[str, Any]],
        capability_events: list[dict[str, Any]] | None = None,
    ) -> None:
        self.initialize()
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute(
                "INSERT INTO monitor_runs (collected_at, timezone, commit_window_json) VALUES (?, ?, ?)",
                (collected_at, timezone, json.dumps(commit_window, ensure_ascii=False)),
            )
            run_id = int(cursor.lastrowid)
            for project in projects:
                versions = project.get("versions") if isinstance(project.get("versions"), dict) else {}
                pypi = versions.get("pypi") if isinstance(versions.get("pypi"), dict) else {}
                release = versions.get("github_release") if isinstance(versions.get("github_release"), dict) else {}
                conn.execute(
                    """
                    INSERT INTO project_snapshots (
                        run_id, project_id, project_name, pypi_version, github_release_version,
                        github_release_published_at, github_release_url, commit_count, issue_count,
                        raw_payload_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        project["id"],
                        project["name"],
                        pypi.get("current"),
                        release.get("current"),
                        release.get("published_at"),
                        release.get("html_url"),
                        project.get("daily_commit_count", 0),
                        project.get("popular_issue_count", 0),
                        json.dumps(project, ensure_ascii=False),
                    ),
                )
            for event in capability_events or []:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO capability_events (
                        run_id, project_id, project_name, capability_id, capability_name,
                        release_tag, release_published_at, status, evidence_text, evidence_url,
                        matched_keywords_json, confidence
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id, event["project_id"], event["project_name"], event["capability_id"],
                        event["capability_name"], event["release_tag"], event.get("release_published_at"), event["status"],
                        event["evidence_text"], event.get("evidence_url"),
                        json.dumps(event.get("matched_keywords", []), ensure_ascii=False), event["confidence"],
                    ),
                )

    def latest_capability_matrix(self) -> dict[tuple[str, str], dict[str, Any]]:
        self.initialize()
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                """
                SELECT project_id, capability_id, release_tag, status, evidence_text, evidence_url, confidence
                FROM (
                    SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY project_id, capability_id
                        ORDER BY COALESCE(release_published_at, '') DESC, id DESC
                    ) AS rank
                    FROM capability_events
                ) WHERE rank = 1
                """
            ).fetchall()
        return {
            (row[0], row[1]): {
                "release_tag": row[2], "status": row[3], "evidence_text": row[4],
                "evidence_url": row[5], "confidence": row[6],
            }
            for row in rows
        }

    def latest_project_payload(self, project_id: str) -> dict[str, Any] | None:
        self.initialize()
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                "SELECT raw_payload_json FROM project_snapshots WHERE project_id = ? ORDER BY run_id DESC LIMIT 20",
                (project_id,),
            ).fetchall()
        for row in rows:
            try:
                payload = json.loads(row[0])
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and isinstance(payload.get("release_catalog"), list) and payload["release_catalog"]:
                return payload
        return None
