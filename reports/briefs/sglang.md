# TECHNOLOGY BRIEF / 2026.07

# SGLang 版本演进简报

> 基于官方 GitHub Releases 的版本、Feature 与技术路线归纳。

**一句话结论**：SGLang 的版本演进以 稳定性与可观测性、性能与资源效率、调度与并行 为主要证据主线；结论仅覆盖官方 Release 明确披露的能力。

**最新正式版本**：[v0.5.15](https://github.com/sgl-project/sglang/releases/tag/v0.5.15)（2026-07-10）。
**最新稳定补丁**：[v0.5.15.post1](https://github.com/sgl-project/sglang/releases/tag/v0.5.15.post1)（2026-07-14）。

## 01 版本演进时间线

| 阶段 | 时间 | 代表版本 | 核心主题 |
|---|---|---|---|
| 阶段 1：0.1.x | 2024-01-18–2024-07-14 | v0.1.5–v0.1.20 | 稳定性与可观测性、推理服务 API、调度与并行 |
| 阶段 2：0.2.x | 2024-07-25–2024-09-19 | v0.2.0–v0.2.13 | 硬件与后端、性能与资源效率、推理服务 API |
| 阶段 3：0.3.x | 2024-09-19–2024-11-22 | v0.3.0–v0.3.6 | 模型能力、硬件与后端、推理服务 API |
| 阶段 4：0.4.x | 2024-12-04–2025-07-31 | v0.4.0–v0.4.10 | 模型能力、硬件与后端、调度与并行 |
| 阶段 5：0.5.x | 2025-08-23–2026-07-14 | v0.5.1–v0.5.15.post1 | 硬件与后端、调度与并行、性能与资源效率 |

## 02 核心判断

| 技术主线 | 证据路径 |
|---|---|
| 性能与缓存 | v0.1.6 → v0.5.15；性能与资源效率、量化与 KV Cache |
| 调度、并行与集群 | v0.1.6 → v0.5.15；调度与并行 |
| 模型、架构与服务接口 | v0.1.6 → v0.5.15；硬件与后端、推理服务 API、模型能力 |

## 03 关键版本里程碑

| 时间 | 版本 | 版本意义 / 关键 Feature |
|---:|---|---|
| 2024-01-18 | [v0.1.5](https://github.com/sgl-project/sglang/releases/tag/v0.1.5) | Fix for T4 GPUs by @Ying1123 in https://github.com/sgl-project/sglang/pull/16 |
| 2024-07-14 | [v0.1.20](https://github.com/sgl-project/sglang/releases/tag/v0.1.20) | Add Qwen2 MoE support by @M0gician in https://github.com/sgl-project/sglang/pull/603 |
| 2024-07-25 | [v0.2.0](https://github.com/sgl-project/sglang/releases/tag/v0.2.0) | Add support for OpenAI API parallel sampling by @yichuan520030910320 in https://github.com/sgl-project/sglang/pull/640 |
| 2024-10-02 | [v0.3.2](https://github.com/sgl-project/sglang/releases/tag/v0.3.2) | Add Support for XVERSE Models (Dense and MoE) to sglang by @hxer7963 in https://github.com/sgl-project/sglang/pull/1397 |
| 2025-03-13 | [v0.4.4](https://github.com/sgl-project/sglang/releases/tag/v0.4.4) | **Enhanced FlashInfer MLA Support**: Now fully compatible with radix cache, chunked prefill, and MTP optimizations - enable with |
| 2025-04-07 | [v0.4.5](https://github.com/sgl-project/sglang/releases/tag/v0.4.5) | The SGLang team is excited to the release of v0.4.5! This version introduces several significant features, including Llama 4 support, FlashAttention 3 backend, EAGLE3 speculative d |
| 2025-09-12 | [v0.5.2](https://github.com/sgl-project/sglang/releases/tag/v0.5.2) | add variable TP Decode > Prefill size support by @shaharmor98 in https://github.com/sgl-project/sglang/pull/9960 |
| 2025-12-03 | [v0.5.6](https://github.com/sgl-project/sglang/releases/tag/v0.5.6) | feat: Add FP4 (E2M1) KV Cache Support for MHA by @JackChuang in https://github.com/sgl-project/sglang/pull/12612 |
| 2026-01-01 | [v0.5.7](https://github.com/sgl-project/sglang/releases/tag/v0.5.7) | [model-gateway] feat: add DAG parallel execution support and workflow optimization by @slin1237 in https://github.com/sgl-project/sglang/pull/14999 |
| 2026-01-23 | [v0.5.8](https://github.com/sgl-project/sglang/releases/tag/v0.5.8) | [model-gateway] feat: add DAG parallel execution support and workflow optimization by @slin1237 in https://github.com/sgl-project/sglang/pull/14999 |
| 2026-04-06 | [v0.5.10](https://github.com/sgl-project/sglang/releases/tag/v0.5.10) | **Qwen3.5 GDN/KDA Optimization**: Transpose linear attention state layout from [N, HV, K, V] to [N, HV, V, K] and fuse split/reshape/cat ops in GDN projection with Triton kernel, p |
| 2026-07-10 | [v0.5.15](https://github.com/sgl-project/sglang/releases/tag/v0.5.15) | [XPU] Enable XPU graph support (decode full-graph + prefill tc_piecewise): [#29053](https://github.com/sgl-project/sglang/pull/29053) |

## 04 技术选型启示

- **适合重点评估的场景**：需要 稳定性与可观测性、性能与资源效率、调度与并行 相关能力，且接受较快版本节奏的部署环境。
- **生产部署注意**：固定镜像、依赖与 Kernel 组合；将 stable、post/patch 与 rc/prerelease 分开验证。
- **比较边界**：本简报说明官方披露的演进证据，不构成跨框架性能排名或兼容性承诺。

## 05 版本与证据说明

- **资料来源**：[官方 GitHub Releases](https://github.com/sgl-project/sglang/releases)
- **截止日期**：2026-07-18；发布日期按 UTC 统计。
- **版本筛选**：仅纳入非 draft、非 prerelease 且 tag 以 `v` 开头的主项目 Release。
- **证据边界**：未命中能力词典时标记为待复核，不等同于不支持。
