# TECHNOLOGY BRIEF / 2026.07

# TensorRT-LLM 版本演进简报

> 基于官方 GitHub Releases 的版本、Feature 与技术路线归纳。

**一句话结论**：TensorRT-LLM 的版本演进以 硬件与后端、量化与 KV Cache、性能与资源效率 为主要证据主线；结论仅覆盖官方 Release 明确披露的能力。

**最新正式版本**：[v1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1)（2026-04-20）。
**最新稳定补丁**：当前 Release 列表未单独识别到 post/patch 发布。

## 01 版本演进时间线

| 阶段 | 时间 | 代表版本 | 核心主题 |
|---|---|---|---|
| 阶段 1：0.5.x | 2023-10-19–2024-02-29 | v0.5.0–v0.8.0 | 硬件与后端、量化与 KV Cache、性能与资源效率 |
| 阶段 2：0.9.x | 2024-04-16–2024-08-29 | v0.9.0–v0.12.0 | 模型能力、硬件与后端、调度与并行 |
| 阶段 3：0.13.x | 2024-09-30–2024-12-24 | v0.13.0–v0.16.0 | 硬件与后端、量化与 KV Cache、性能与资源效率 |
| 阶段 4：0.17.x | 2025-02-07–2025-06-19 | v0.17.0–v0.20.0 | 硬件与后端、模型能力、调度与并行 |
| 阶段 5：0.21.x | 2025-08-04–2026-04-20 | v0.21.0–v1.2.1 | 量化与 KV Cache、模型能力、硬件与后端 |

## 02 核心判断

| 技术主线 | 证据路径 |
|---|---|
| 性能与缓存 | v0.6.1 → v1.2.1；量化与 KV Cache、性能与资源效率 |
| 调度、并行与集群 | v0.9.0 → v1.2.0；调度与并行 |
| 模型、架构与服务接口 | v0.6.1 → v1.2.0；硬件与后端、模型能力、推理服务 API |

## 03 关键版本里程碑

| 时间 | 版本 | 版本意义 / 关键 Feature |
|---:|---|---|
| 2023-12-04 | [v0.6.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.6.1) | We are updating the main branch regularly with new features, bug fixes and performance optimizations. The stable branch will be updated less frequently. The exact frequencies depen |
| 2024-02-29 | [v0.8.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.8.0) | Custom allreduce performance optimization by introducing a ping-pong buffer to avoid an extra synchronization cost |
| 2024-04-16 | [v0.9.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.9.0) | We are updating the main branch regularly with new features, bug fixes and performance optimizations. The stable branch will be updated less frequently, and the exact frequencies d |
| 2024-06-05 | [v0.10.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.10.0) | We are updating the `main` branch regularly with new features, bug fixes and performance optimizations. The `rel` branch will be updated less frequently, and the exact frequencies  |
| 2024-07-17 | [v0.11.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.11.0) | We are updating the `main` branch regularly with new features, bug fixes and performance optimizations. The `rel` branch will be updated less frequently, and the exact frequencies  |
| 2024-09-30 | [v0.13.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.13.0) | We are updating the `main` branch regularly with new features, bug fixes and performance optimizations. The `rel` branch will be updated less frequently, and the exact frequencies  |
| 2024-12-04 | [v0.15.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.15.0) | We are updating the `main` branch regularly with new features, bug fixes and performance optimizations. The `rel` branch will be updated less frequently, and the exact frequencies  |
| 2024-12-24 | [v0.16.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.16.0) | We are updating the `main` branch regularly with new features, bug fixes and performance optimizations. The `rel` branch will be updated less frequently, and the exact frequencies  |
| 2025-05-09 | [v0.19.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v0.19.0) | Added INT4-AWQ support for MoE models. Refer to the “AWQ Quantization” section in `examples/mixtral/README.md`. |
| 2025-09-24 | [v1.0.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0) | [None][doc] add blackwell information into support matrix by @nv-guomingz in https://github.com/NVIDIA/TensorRT-LLM/pull/6740 |
| 2025-12-19 | [v1.1.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.1.0) | [TRTLLM-6420][feat] add support for Eclairv2 model - cherry-pick changes and minor fix by @yibinl-nvidia in https://github.com/NVIDIA/TensorRT-LLM/pull/6493 |
| 2026-04-20 | [v1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1) | Fixed an issue that caused KV cache corruption (#12770) |

## 04 技术选型启示

- **适合重点评估的场景**：需要 硬件与后端、量化与 KV Cache、性能与资源效率 相关能力，且接受较快版本节奏的部署环境。
- **生产部署注意**：固定镜像、依赖与 Kernel 组合；将 stable、post/patch 与 rc/prerelease 分开验证。
- **比较边界**：本简报说明官方披露的演进证据，不构成跨框架性能排名或兼容性承诺。

## 05 版本与证据说明

- **资料来源**：[官方 GitHub Releases](https://github.com/NVIDIA/TensorRT-LLM/releases)
- **截止日期**：2026-07-18；发布日期按 UTC 统计。
- **版本筛选**：仅纳入非 draft、非 prerelease 且 tag 以 `v` 开头的主项目 Release。
- **证据边界**：未命中能力词典时标记为待复核，不等同于不支持。
