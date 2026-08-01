from pathlib import Path


def test_daily_workflow_publishes_canonical_reports():
    root = Path(__file__).parents[1]
    workflow = (root / ".github/workflows/vllm-monitor.yml").read_text(
        encoding="utf-8"
    )

    assert "contents: write" in workflow
    assert 'echo "cutoff=$(date -u +%F)"' in workflow
    assert '--cutoff "${{ steps.run.outputs.cutoff }}"' in workflow
    assert "--run-id" not in workflow
    assert "git diff --quiet -- data/raw" in workflow
    assert "git add data/raw" in workflow
    assert 'git push origin "HEAD:${GITHUB_REF_NAME}"' in workflow
    assert "output/vllm/build_manifest.json" in workflow
    assert "output/sglang/build_manifest.json" in workflow
