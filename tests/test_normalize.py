import json
from pathlib import Path
from release_report.config import load_config
from release_report.normalize import normalize_releases

def test_normalize_release_kinds_and_cutoff():
    root = Path(__file__).parents[1]
    records = normalize_releases(json.loads((root / 'tests/fixtures/releases.json').read_text()), load_config(root / 'config/vllm.yaml'), '2024-02-10')
    assert [record.release_kind for record in records] == ['stable', 'rc', 'stable']
    assert records[-1].tag == 'v0.2.0'
