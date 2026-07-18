# TECHNOLOGY BRIEF / 2026.07

# vLLM 版本演进简报

> 基于官方 GitHub Releases 的版本、Feature 与技术路线归纳。

**一句话结论**：vLLM 的版本演进以 稳定性与可观测性、硬件与后端、量化与 KV Cache 为主要证据主线；结论仅覆盖官方 Release 明确披露的能力。

**最新正式版本**：[v0.25.1](https://github.com/vllm-project/vllm/releases/tag/v0.25.1)（2026-07-14）。
**最新稳定补丁**：当前 Release 列表未单独识别到 post/patch 发布。

## 01 版本演进时间线

| 阶段 | 时间 | 代表版本 | 核心主题 |
|---|---|---|---|
| 阶段 1：0.1.x | 2023-06-20–2024-08-23 | v0.1.0–v0.5.5 | 稳定性与可观测性、硬件与后端、推理服务 API |
| 阶段 2：0.6.x | 2024-09-04–2025-09-13 | v0.6.0–v0.10.2 | 稳定性与可观测性、模型能力、硬件与后端 |
| 阶段 3：0.11.x | 2025-10-02–2026-02-04 | v0.11.0–v0.15.1 | 稳定性与可观测性、模型能力、性能与资源效率 |
| 阶段 4：0.16.x | 2026-02-25–2026-05-10 | v0.16.0–v0.20.2 | 模型能力、量化与 KV Cache、稳定性与可观测性 |
| 阶段 5：0.21.x | 2026-05-15–2026-07-14 | v0.21.0–v0.25.1 | 量化与 KV Cache、稳定性与可观测性、硬件与后端 |

## 02 核心判断

| 技术主线 | 证据路径 |
|---|---|
| 性能与缓存 | v0.1.4 → v0.25.1；量化与 KV Cache、性能与资源效率 |
| 调度、并行与集群 | v0.1.3 → v0.25.0；调度与并行 |
| 模型、架构与服务接口 | v0.1.2 → v0.25.0；硬件与后端、推理服务 API、模型能力 |

## 03 关键版本里程碑

| 时间 | 版本 | 版本意义 / 关键 Feature |
|---:|---|---|
| 2023-06-22 | [v0.1.1](https://github.com/vllm-project/vllm/releases/tag/v0.1.1) | [Bugfix] Fix a bug in RequestOutput.finished by @WoosukKwon in https://github.com/vllm-project/vllm/pull/202 |
| 2024-03-30 | [v0.4.0](https://github.com/vllm-project/vllm/releases/tag/v0.4.0) | [Fix] Add args for mTLS support by @declark1 in https://github.com/vllm-project/vllm/pull/3430 |
| 2024-12-17 | [v0.6.5](https://github.com/vllm-project/vllm/releases/tag/v0.6.5) | Major improvements in `torch.compile` integration: Support for all attention backends, encoder-based models, dynamic FP8 fusion, shape specialization fixes, and performance optimiz |
| 2025-03-18 | [v0.8.0](https://github.com/vllm-project/vllm/releases/tag/v0.8.0) | [FEAT] [ROCm] [Embedding] Add encoder-only model support into ROCm Flash Attention to enable embedding models. by @tjtanaa in https://github.com/vllm-project/vllm/pull/14664 |
| 2025-06-10 | [v0.9.1](https://github.com/vllm-project/vllm/releases/tag/v0.9.1) | FP4: Add compressed-tensors NVFP4 support (#18312), FP4 MoE kernel optimization (#19110) |
| 2025-07-24 | [v0.10.0](https://github.com/vllm-project/vllm/releases/tag/v0.10.0) | Hardware-specific: FP8 KV cache quantization on TPU (#19292), FP8 support for BatchedTritonExperts (#18864), optimized INT8 vectorization kernels (#20331). |
| 2025-08-18 | [v0.10.1](https://github.com/vllm-project/vllm/releases/tag/v0.10.1) | **Performance and compatibility improvements**: CUDA kernel optimization for Int8 per-token group quantization (#21476), non-contiguous tensor support in FP8 quantization (#21961), |
| 2025-09-13 | [v0.10.2](https://github.com/vllm-project/vllm/releases/tag/v0.10.2) | **Performance core improvements**: `--safetensors-load-strategy` for NFS based file loading acceleration (#24469), critical CUDA graph capture throughput fix (#24128), scheduler op |
| 2025-11-18 | [v0.11.1](https://github.com/vllm-project/vllm/releases/tag/v0.11.1) | [Hardware][AMD][Model] Add Triton MoE tuning support and optimized configs for Qwen3 omni for MI308X (@sammysun0711 #28373) |
| 2026-04-27 | [v0.20.0](https://github.com/vllm-project/vllm/releases/tag/v0.20.0) | **Performance**: Optimize batch invariant with fused rms norm — 2.1% E2E latency improvement (#40413); avoid `seq_lens_cpu` GPU→CPU sync (#40654); cache `InductorPass.hash_source`  |
| 2026-06-15 | [v0.23.0](https://github.com/vllm-project/vllm/releases/tag/v0.23.0) | **DeepSeek-V4 matures across backends**: Following its introduction in v0.22.0, DeepSeek-V4 received another large hardening and optimization pass. Its sparse MLA metadata is now d |
| 2026-07-14 | [v0.25.1](https://github.com/vllm-project/vllm/releases/tag/v0.25.1) | v0.25.1 is a patch release containing two targeted bug fixes on top of v0.25.0. |

## 04 技术选型启示

- **适合重点评估的场景**：需要 稳定性与可观测性、硬件与后端、量化与 KV Cache 相关能力，且接受较快版本节奏的部署环境。
- **生产部署注意**：固定镜像、依赖与 Kernel 组合；将 stable、post/patch 与 rc/prerelease 分开验证。
- **比较边界**：本简报说明官方披露的演进证据，不构成跨框架性能排名或兼容性承诺。

## 05 版本与证据说明

- **资料来源**：[官方 GitHub Releases](https://github.com/vllm-project/vllm/releases)
- **截止日期**：2026-07-18；发布日期按 UTC 统计。
- **版本筛选**：仅纳入非 draft、非 prerelease 且 tag 以 `v` 开头的主项目 Release。
- **证据边界**：未命中能力词典时标记为待复核，不等同于不支持。
