from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import requests

from .config import Config


class FetchError(RuntimeError):
    pass


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp = Path(handle.name)
    temp.replace(path)


def cache_path(config: Config) -> Path:
    return config.path.parent.parent / "data" / "raw" / f"{config.project['repository']}_releases.json"


def fetch_releases(config: Config, offline: bool = False) -> dict[str, Any]:
    path = cache_path(config)
    if offline:
        if not path.exists():
            raise FetchError(f"Offline cache not found: {path}")
        cached = json.loads(path.read_text(encoding="utf-8"))
        cached["source_mode"] = "cache"
        return cached

    prior = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "release-report/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    metadata = prior.get("metadata", {}) if isinstance(prior, dict) else {}
    if metadata.get("etag"):
        headers["If-None-Match"] = metadata["etag"]
    url = f"https://api.github.com/repos/{config.repo_slug}/releases"
    releases: list[Any] = []
    session = requests.Session()
    for page in range(1, 100):
        response = None
        for attempt in range(4):
            response = session.get(url, headers=headers, params={"per_page": 100, "page": page}, timeout=30)
            if response.status_code not in (429, 500, 502, 503, 504):
                break
            time.sleep(min(8, 2**attempt))
        assert response is not None
        if response.status_code == 304 and prior:
            prior["source_mode"] = "cache"
            return prior
        if response.status_code >= 400:
            if prior:
                prior["source_mode"] = "cache_rate_limited"
                return prior
            raise FetchError(f"GitHub releases fetch failed: HTTP {response.status_code}")
        page_data = response.json()
        if not isinstance(page_data, list):
            raise FetchError("GitHub releases response was not a list")
        releases.extend(page_data)
        if len(page_data) < 100:
            retrieved_at = datetime.now(timezone.utc).isoformat()
            payload = {
                "metadata": {"source_url": url, "retrieved_at": retrieved_at, "etag": response.headers.get("ETag"), "last_modified": response.headers.get("Last-Modified")},
                "releases": releases,
                "source_mode": "live",
            }
            _atomic_json(path, payload)
            return payload
    raise FetchError("GitHub releases pagination exceeded safe page limit")
