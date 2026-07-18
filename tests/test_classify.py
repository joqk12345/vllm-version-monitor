import json
from pathlib import Path
from release_report.classify import classify
from release_report.config import load_config
from release_report.normalize import normalize_releases

def test_taxonomy_classification():
    root = Path(__file__).parents[1]; config = load_config(root / 'config/vllm.yaml')
    features = classify(normalize_releases(json.loads((root / 'tests/fixtures/releases.json').read_text()), config), config)
    assert {'kv_cache_memory', 'scheduling_batching', 'api_protocol'} <= {feature.category for feature in features}
