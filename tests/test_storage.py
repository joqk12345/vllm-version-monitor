import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))

from projects import load_projects
from storage import MonitorStore
from capabilities import _matches_keyword, extract_capability_events, load_capabilities, render_capability_matrix
from project_detail import render_project_detail
from evolution_brief import render_evolution_brief
from report import _build_report


class MonitorStoreTest(unittest.TestCase):
    def test_config_and_latest_versions(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(
            [project.id for project in load_projects(root / "config" / "projects.json")],
            ["vllm", "sglang", "tensorrt_llm"],
        )
        with tempfile.TemporaryDirectory() as directory:
            store = MonitorStore(Path(directory) / "history.db")
            store.save_run(
                collected_at="2026-07-18T00:00:00+00:00",
                timezone="UTC",
                commit_window={"since_utc": "2026-07-18T00:00:00Z"},
                projects=[
                    {
                        "id": "vllm",
                        "name": "vLLM",
                        "versions": {
                            "pypi": {"current": "1.0.0"},
                            "github_release": {"current": "v1.0.0"},
                        },
                    }
                ],
            )
            self.assertEqual(
                store.latest_versions("vllm"),
                {"pypi_version": "1.0.0", "github_release_version": "v1.0.0"},
            )

    def test_release_notes_become_traceable_capability_events(self) -> None:
        root = Path(__file__).resolve().parents[1]
        capabilities = load_capabilities(root / "config" / "capabilities.json")
        project = {
            "id": "vllm", "name": "vLLM",
            "versions": {"github_release": {"current": "v1.2.0", "html_url": "https://example.test/release"}},
            "latest_release_notes": "- Add experimental FP8 KV cache support\n- Improve scheduler throughput",
        }
        events = extract_capability_events(project, capabilities)
        self.assertEqual({event["capability_id"] for event in events}, {"quantization", "scheduling_parallelism", "performance"})
        self.assertTrue(all(event["evidence_url"] == "https://example.test/release" for event in events))
        matrix = {("vllm", event["capability_id"]): event for event in events}
        markdown = render_capability_matrix([project], capabilities, matrix)
        self.assertIn("experimental (v1.2.0)", markdown)

    def test_short_keywords_do_not_match_inside_unrelated_words(self) -> None:
        self.assertFalse(_matches_keyword("output logprobs", "tpu"))
        self.assertTrue(_matches_keyword("TPU backend support", "tpu"))

    def test_report_renders_capability_matrix(self) -> None:
        report, _, _ = _build_report(
            date="2026-07-18",
            data={
                "capability_matrix_markdown": "| 能力 | vLLM |\n|---|---|\n| 量化与 KV Cache | experimental (v1.2.0) |",
                "capability_events": [{}],
            },
            pipeline_log=None,
            change_report=None,
            verify_report=None,
            cost_log=None,
            state_data=None,
        )
        self.assertIn("## Framework Capability Matrix", report)
        self.assertIn("Release-note capability evidence evaluated this run: 1", report)

    def test_report_makes_collection_errors_prominent(self) -> None:
        report, summary, _ = _build_report(
            date="2026-07-18", data={"errors": ["GitHub release example: timeout"]},
            pipeline_log=None, change_report=None, verify_report=None, cost_log=None, state_data=None,
        )
        self.assertIn("collection errors", summary)
        self.assertIn("## Errors", report)
        self.assertIn("GitHub release example: timeout", report)

    def test_project_detail_has_version_timeline_and_evidence(self) -> None:
        root = Path(__file__).resolve().parents[1]
        capabilities = load_capabilities(root / "config" / "capabilities.json")
        project = {
            "id": "sglang", "name": "SGLang",
            "versions": {
                "pypi": {"current": "0.5.15"},
                "github_release": {"current": "v0.5.15", "html_url": "https://example.test/latest", "published_at": "2026-07-10T00:00:00Z"},
            },
        }
        releases = [
            {"tag_name": "v0.4.0", "published_at": "2025-01-01T00:00:00Z", "html_url": "https://example.test/040", "body": "- Add chunked prefill scheduler"},
            {"tag_name": "v0.5.15", "published_at": "2026-07-10T00:00:00Z", "html_url": "https://example.test/0515", "body": "- Enable experimental FP8 KV cache"},
        ]
        detail = render_project_detail(project, releases, capabilities)
        self.assertIn("# SGLang 版本与 Feature 明细", detail)
        self.assertIn("### 0.4.x", detail)
        self.assertIn("### 0.5.x", detail)
        self.assertIn("## 关键 Feature 的首次与最近证据", detail)
        self.assertLess(detail.index("v0.4.0："), detail.index("v0.5.15："))

    def test_evolution_brief_has_editorial_sections(self) -> None:
        root = Path(__file__).resolve().parents[1]
        capabilities = load_capabilities(root / "config" / "capabilities.json")
        project = {"id": "sglang", "name": "SGLang", "github_repo": "sgl-project/sglang", "versions": {"github_release": {}}}
        releases = [
            {"tag_name": "v0.1.6", "published_at": "2024-01-21T00:00:00Z", "html_url": "https://example.test/016", "body": "- Add OpenAI-compatible API server"},
            {"tag_name": "v0.5.15", "published_at": "2026-07-10T00:00:00Z", "html_url": "https://example.test/0515", "body": "- Enable CUDA graph and improve throughput"},
            {"tag_name": "v0.5.15.post1", "published_at": "2026-07-14T00:00:00Z", "html_url": "https://example.test/0515p1", "body": "- Fix CUDA graph regression"},
        ]
        brief = render_evolution_brief(project, releases, capabilities, "2026-07-18")
        self.assertIn("## 01 版本演进时间线", brief)
        self.assertIn("## 03 关键版本里程碑", brief)
        self.assertIn("最新稳定补丁", brief)


if __name__ == "__main__":
    unittest.main()
