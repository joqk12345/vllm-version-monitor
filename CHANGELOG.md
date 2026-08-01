# Changelog

本文件记录 Release Intelligence 管线的重要变更。

## [Unreleased]

### Fixed

- 修复每日工作流只上传 Actions artifact、未将最新 canonical 报告写回仓库的问题。
- 每日构建显式使用当天 UTC 日期作为 cutoff，避免配置中的历史固定日期让最新 stable 长期停滞。
- GitHub Releases 缓存改为只保留报告实际消费的证据字段，忽略 asset 下载次数等易变元数据，避免无实质变化时反复提交二进制报告。

### Changed

- 每日工作流获得最小 `contents: write` 权限，并在官方 release 证据变化时由 `github-actions[bot]` 提交 `data/raw/` 与 canonical `output/<project>/`。
- 新增工作流并发控制、无变化跳过逻辑和对应回归测试；timestamped artifact 保留期调整为 90 天。
- `--run-id` 保留为本地或临时归档能力；每日持久状态改由 canonical manifest 表达，不再向 Git 历史追加 `runs/` 目录。

### Verified

- 修复后的首次远端运行成功把 vLLM manifest 从 `v0.25.1` 更新到 `v0.26.0`，cutoff 更新为 `2026-08-01`。
- 连续无变化运行成功跳过仓库提交，同时继续完成测试、报告验证和 artifact 上传。

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
