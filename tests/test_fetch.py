import json
from pathlib import Path

from release_report.config import load_config
from release_report.fetch import canonical_release_evidence, fetch_releases


def test_canonical_release_evidence_ignores_volatile_asset_metadata():
    release = {
        "tag_name": "v0.26.0",
        "published_at": "2026-07-27T01:06:58Z",
        "created_at": "2026-07-27T00:00:00Z",
        "draft": False,
        "prerelease": False,
        "html_url": "https://github.com/vllm-project/vllm/releases/tag/v0.26.0",
        "body": "release evidence",
        "assets": [{"name": "wheel.whl", "download_count": 42}],
        "author": {"login": "maintainer"},
    }

    first = canonical_release_evidence([release])
    release["assets"][0]["download_count"] = 43
    release["author"]["login"] = "renamed-maintainer"
    second = canonical_release_evidence([release])

    assert first == second
    assert first == [
        {
            "tag_name": "v0.26.0",
            "published_at": "2026-07-27T01:06:58Z",
            "created_at": "2026-07-27T00:00:00Z",
            "draft": False,
            "prerelease": False,
            "html_url": "https://github.com/vllm-project/vllm/releases/tag/v0.26.0",
            "body": "release evidence",
        }
    ]


def test_fetch_does_not_rewrite_cache_for_volatile_only_changes(
    tmp_path, monkeypatch
):
    root = Path(__file__).parents[1]
    config = load_config(root / "config/vllm.yaml")
    cache = tmp_path / "releases.json"
    release = {
        "tag_name": "v0.26.0",
        "published_at": "2026-07-27T01:06:58Z",
        "created_at": "2026-07-27T00:00:00Z",
        "draft": False,
        "prerelease": False,
        "html_url": "https://github.com/vllm-project/vllm/releases/tag/v0.26.0",
        "body": "release evidence",
        "assets": [{"download_count": 42}],
    }
    cached = {
        "metadata": {"retrieved_at": "2026-08-01T00:00:00+00:00"},
        "releases": [release],
        "source_mode": "live",
    }
    cache.write_text(json.dumps(cached), encoding="utf-8")
    original = cache.read_bytes()

    current = json.loads(json.dumps(release))
    current["assets"][0]["download_count"] = 43

    class Response:
        status_code = 200
        headers = {"ETag": "new-etag", "Last-Modified": None}

        @staticmethod
        def json():
            return [current]

    class Session:
        @staticmethod
        def get(*args, **kwargs):
            return Response()

    monkeypatch.setattr("release_report.fetch.cache_path", lambda unused: cache)
    monkeypatch.setattr("release_report.fetch.requests.Session", Session)

    result = fetch_releases(config)

    assert result["source_mode"] == "cache"
    assert cache.read_bytes() == original
