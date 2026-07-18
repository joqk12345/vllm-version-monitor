from pathlib import Path

from release_report.config import load_config
from release_report.cli import _paths
from release_report.manifest import validate_manifest, write_manifest


def test_build_manifest_schema_and_hashes(tmp_path):
    root = Path(__file__).parents[1]
    config = load_config(root / "config/vllm.yaml")
    artifacts = []
    for relative in ("json/releases.json", "json/milestones.json", "pdf/detail.pdf", "pdf/brief.pdf"):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"test artifact content")
        artifacts.append(path)
    write_manifest(tmp_path, config, "2026-07-18", "fixture", "v0.25.1", artifacts)
    manifest = validate_manifest(tmp_path, root / "schemas")
    assert manifest["latest_stable"] == "v0.25.1"


def test_run_id_scopes_output_paths():
    root = Path(__file__).parents[1]
    config = load_config(root / "config/vllm.yaml")
    output_root, json_dir, pdf_dir, qa_dir = _paths(config, "2026-07-18T11-30-00Z")
    assert output_root == root / "output/vllm/runs/2026-07-18T11-30-00Z"
    assert json_dir == output_root / "json"
    assert pdf_dir == output_root / "pdf"
    assert qa_dir == output_root / "qa"
