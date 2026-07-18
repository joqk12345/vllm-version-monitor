import json
from pathlib import Path
from release_report.config import load_config
from release_report.normalize import normalize_releases
from release_report.stages import build_stages

def test_stage_override():
    root = Path(__file__).parents[1]; config = load_config(root / 'config/vllm.yaml')
    stages = build_stages(normalize_releases(json.loads((root / 'tests/fixtures/releases.json').read_text()), config), config)
    assert stages[0].name == 'Foundation'
