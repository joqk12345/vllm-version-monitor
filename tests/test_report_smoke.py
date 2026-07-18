import json
from pathlib import Path

from release_report.classify import classify
from release_report.config import load_config
from release_report.normalize import normalize_releases
from release_report.render_brief import render_brief
from release_report.stages import build_stages


def test_brief_pdf_smoke(tmp_path):
    root = Path(__file__).parents[1]
    config = load_config(root / "config/vllm.yaml")
    records = normalize_releases(json.loads((root / "tests/fixtures/releases.json").read_text()), config)
    output = tmp_path / "brief.pdf"
    render_brief(output, config, records, classify(records, config), build_stages(records, config), "2024-02-11")
    assert output.exists() and output.stat().st_size > 1000
