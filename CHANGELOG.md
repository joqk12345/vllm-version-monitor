# Changelog

本文件记录 Release Intelligence 管线的重要变更。

## [0.2.0] - 2026-07-18

**Release tag:** `v0.2.0` (create after the release commit is made).

### Added

- 配置驱动的 vLLM 与 SGLang Release Intelligence PDF 管线。
- `release-report` CLI：`fetch`、`analyze`、`render`、`verify`、`build`。
- GitHub Release 分页抓取、缓存、离线重建、版本规范化和 Feature taxonomy。
- A4 详细项目分析 PDF、严格两页的 A4 横向 Evolution Brief。
- PDF 逐页渲染、contact sheet、文本/元数据检查和 SHA-256 验证。
- `build_manifest.json`、`verification.json` 及对应 JSON schemas。
- 每日 GitHub Actions：测试、双项目构建、验证与 artifact 上传。

### Changed

- 主工作流从旧的 Markdown 监控升级为可验证的 PDF Release Intelligence 构建。
- 输出改为 `output/vllm/` 和 `output/sglang/` 的独立 artifact 树，避免项目互相覆盖。

## 2026-07-18

### Added

- 初始 vLLM 版本监控技能与日常 Markdown 报告原型。
