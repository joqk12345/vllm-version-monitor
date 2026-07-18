# vLLM 版本与 Feature 明细

## 当前状态

- GitHub Release：[v0.25.1](https://github.com/vllm-project/vllm/releases/tag/v0.25.1)
- 发布时间：2026-07-14T08:51:20Z
- PyPI：`0.25.1`
- 历史 Releases：91 条（仅含 GitHub 正式 Release，draft 已排除）

## 版本演进总览

以下按 GitHub Release 的 `major.minor` 分组。Feature 描述保留 release note 原文，便于回溯验证。

### 0.1.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.1.0](https://github.com/vllm-project/vllm/releases/tag/v0.1.0) | 2023-06-20 | Release notes 未匹配到已配置能力关键词 |
| [v0.1.1](https://github.com/vllm-project/vllm/releases/tag/v0.1.1) | 2023-06-22 | [Bugfix] Fix a bug in RequestOutput.finished by @WoosukKwon in https://github.com/vllm-project/vllm/pull/202 |
| [v0.1.2](https://github.com/vllm-project/vllm/releases/tag/v0.1.2) | 2023-07-05 | ChatCompletion endpoint in OpenAI demo server<br>Various bug fixes and improvements |
| [v0.1.3](https://github.com/vllm-project/vllm/releases/tag/v0.1.3) | 2023-08-02 | fix: enable trust-remote-code in api server & benchmark. by @gesanqiu in https://github.com/vllm-project/vllm/pull/509<br>fixed tensor parallel is not defined by @MoeedDar in https://github.com/vllm-project/vllm/pull/564<br>fix: enable trust-remote-code in api server & benchmark. by @gesanqiu in https://github.com/vllm-project/vllm/pull/509 |
| [v0.1.4](https://github.com/vllm-project/vllm/releases/tag/v0.1.4) | 2023-08-25 | Optimizing CUDA kernels for paged attention and GELU.<br>Supports tokens and arrays of tokens as inputs to the OpenAI completion API by @wanmok in https://github.com/vllm-project/vllm/pull/715<br>[OPTIMIZATION] Optimizes the single_query_cached_kv_attention kernel by @naed90 in https://github.com/vllm-project/vllm/pull/420 |
| [v0.1.5](https://github.com/vllm-project/vllm/releases/tag/v0.1.5) | 2023-09-07 | Enable request body OpenAPI spec for OpenAI endpoints by @Peilun-Li in https://github.com/vllm-project/vllm/pull/865<br>fix: bug fix when penalties are negative by @pfldy2850 in https://github.com/vllm-project/vllm/pull/913 |
| [v0.1.6](https://github.com/vllm-project/vllm/releases/tag/v0.1.6) | 2023-09-08 | Release notes 未匹配到已配置能力关键词 |
| [v0.1.7](https://github.com/vllm-project/vllm/releases/tag/v0.1.7) | 2023-09-11 | fix: CUDA error when inferencing with Falcon-40B base model by @kyujin-cho in https://github.com/vllm-project/vllm/pull/992<br>A minor release to fix the bugs in ALiBi, Falcon-40B, and Code Llama. |

### 0.2.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.2.0](https://github.com/vllm-project/vllm/releases/tag/v0.2.0) | 2023-09-28 | [Setup] Enable `TORCH_CUDA_ARCH_LIST` for selecting target GPUs by @WoosukKwon in https://github.com/vllm-project/vllm/pull/1074<br>Docs: Fix broken link to openai example by @nkpz in https://github.com/vllm-project/vllm/pull/1145<br>Initial support for AWQ (performance not optimized) |
| [v0.2.1](https://github.com/vllm-project/vllm/releases/tag/v0.2.1) | 2023-10-16 | Fix error message on `TORCH_CUDA_ARCH_LIST` by @WoosukKwon in https://github.com/vllm-project/vllm/pull/1239<br>API server support ipv4 / ipv6 dualstack by @yunfeng-scale in https://github.com/vllm-project/vllm/pull/1288<br>AWQ support for Mistral 7B |
| [v0.2.1.post1](https://github.com/vllm-project/vllm/releases/tag/v0.2.1.post1) | 2023-10-17 | This is an emergency release to fix a bug on tensor parallelism support. |
| [v0.2.2](https://github.com/vllm-project/vllm/releases/tag/v0.2.2) | 2023-11-19 | Fix cpu heavy code in async function _AsyncLLMEngine._run_workers_async by @dominik-schwabe in https://github.com/vllm-project/vllm/pull/1628<br>Return usage for openai requests by @ichernev in https://github.com/vllm-project/vllm/pull/1663<br>Changes in scheduler: from 1D flattened input tensor to 2D tensor |
| [v0.2.3](https://github.com/vllm-project/vllm/releases/tag/v0.2.3) | 2023-12-03 | Rewrite torch.repeat_interleave to remove cpu synchronization by @beginlner in https://github.com/vllm-project/vllm/pull/1599<br>Added echo function to OpenAI API server. by @wanmok in https://github.com/vllm-project/vllm/pull/1504<br>Fix hanging in the scheduler caused by long prompts by @chenxu2048 in https://github.com/vllm-project/vllm/pull/1534 |
| [v0.2.4](https://github.com/vllm-project/vllm/releases/tag/v0.2.4) | 2023-12-11 | [Docker] Add cuda arch list as build option by @simon-mo in https://github.com/vllm-project/vllm/pull/1950<br>Fix OpenAI server completion_tokens referenced before assignment by @js8544 in https://github.com/vllm-project/vllm/pull/1996<br>[Minor] Fix latency benchmark script by @WoosukKwon in https://github.com/vllm-project/vllm/pull/2035 |
| [v0.2.5](https://github.com/vllm-project/vllm/releases/tag/v0.2.5) | 2023-12-14 | [BugFix] Fix input positions for long context with sliding window<br>[Docs] Add notes on ROCm-supported models by @WoosukKwon in https://github.com/vllm-project/vllm/pull/2087<br>Optimize Mixtral performance with expert parallelism (thanks to @Yard1) |
| [v0.2.6](https://github.com/vllm-project/vllm/releases/tag/v0.2.6) | 2023-12-17 | [Docs] Add CUDA graph support to docs by @WoosukKwon in https://github.com/vllm-project/vllm/pull/2148<br>Add GPTQ support by @chu-tianxiang in https://github.com/vllm-project/vllm/pull/916<br>[Docs] Add CUDA graph support to docs by @WoosukKwon in https://github.com/vllm-project/vllm/pull/2148 |
| [v0.2.7](https://github.com/vllm-project/vllm/releases/tag/v0.2.7) | 2024-01-04 | Enable CUDA graph for GPTQ & SqueezeLLM by @WoosukKwon in https://github.com/vllm-project/vllm/pull/2318<br>[BUGFIX] Fix API server test by @zhuohan123 in https://github.com/vllm-project/vllm/pull/2270<br>Fix tensor parallelism support for Mixtral + GPTQ/AWQ |

### 0.3.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.3.0](https://github.com/vllm-project/vllm/releases/tag/v0.3.0) | 2024-01-31 | Optimized MoE performance and Deepseek MoE support<br>[ROCm] add support to ROCm 6.0 and MI300 by @hongxiayang in https://github.com/vllm-project/vllm/pull/2274<br>Support OpenAI API server in `benchmark_serving.py` by @hmellor in https://github.com/vllm-project/vllm/pull/2172 |
| [v0.3.1](https://github.com/vllm-project/vllm/releases/tag/v0.3.1) | 2024-02-16 | Add unit test for Mixtral MoE layer by @pcmoritz in https://github.com/vllm-project/vllm/pull/2677<br>[ROCm] Fix build problem resulted from previous commit related to FP8 kv-cache support  by @hongxiayang in https://github.com/vllm-project/vllm/pull/2…<br>[ROCm] Fix build problem resulted from previous commit related to FP8 kv-cache support  by @hongxiayang in https://github.com/vllm-project/vllm/pull/2… |
| [v0.3.2](https://github.com/vllm-project/vllm/releases/tag/v0.3.2) | 2024-02-21 | [ROCm] include gfx908 as supported by @jamestwhedbee in https://github.com/vllm-project/vllm/pull/2792<br>Add warning to prevent changes to benchmark api server by @simon-mo in https://github.com/vllm-project/vllm/pull/2858<br>[FIX] Add Gemma model to the doc by @zhuohan123 in https://github.com/vllm-project/vllm/pull/2966 |
| [v0.3.3](https://github.com/vllm-project/vllm/releases/tag/v0.3.3) | 2024-03-01 | Performance optimization for MoE kernel<br>Add guided decoding for OpenAI API server by @felixzhu555 in https://github.com/vllm-project/vllm/pull/2819<br>Enables GQA support in the prefix prefill kernels by @sighingnow in https://github.com/vllm-project/vllm/pull/3007 |

### 0.4.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.4.0](https://github.com/vllm-project/vllm/releases/tag/v0.4.0) | 2024-03-30 | [Feature] Add vision language model support. by @xwjiang2010 in https://github.com/vllm-project/vllm/pull/3042<br>[DOC] add setup document to support neuron backend by @liangfu in https://github.com/vllm-project/vllm/pull/2777<br>Support `json_object` in OpenAI server for arbitrary JSON, `--use-delay` flag to improve time to first token across many requests, and `min_tokens` to… |
| [v0.4.0.post1](https://github.com/vllm-project/vllm/releases/tag/v0.4.0.post1) | 2024-04-02 | [Hardware][Intel] Add CPU inference backend by @bigPYJ1151 in https://github.com/vllm-project/vllm/pull/3634<br>[Bugfix] Add `__init__.py` files for `vllm/core/block/` and `vllm/spec_decode/` by @mgoin in https://github.com/vllm-project/vllm/pull/3798<br>[Kernel] Layernorm performance optimization by @mawong-amd in https://github.com/vllm-project/vllm/pull/3662 |
| [v0.4.1](https://github.com/vllm-project/vllm/releases/tag/v0.4.1) | 2024-04-24 | [Misc] Add vision language model support to CPU backend by @Isotr0py in https://github.com/vllm-project/vllm/pull/3968<br>[Frontend] Enable support for CPU backend in AsyncLLMEngine. by @sighingnow in https://github.com/vllm-project/vllm/pull/3993<br>[Bugfix] Remove key sorting for `guided_json` parameter in OpenAi compatible Server by @dmarasco in https://github.com/vllm-project/vllm/pull/3945 |
| [v0.4.2](https://github.com/vllm-project/vllm/releases/tag/v0.4.2) | 2024-05-05 | [Kernel] Optimize FP8 support for MoE kernel / Mixtral via static scales by @pcmoritz in https://github.com/vllm-project/vllm/pull/4343<br>[ROCm][Hardware][AMD] Enable group query attention for triton FA by @hongxiayang in https://github.com/vllm-project/vllm/pull/4406<br>[Frontend] Add --log-level option to api server by @normster in https://github.com/vllm-project/vllm/pull/4377 |
| [v0.4.3](https://github.com/vllm-project/vllm/releases/tag/v0.4.3) | 2024-06-01 | [Bugfix][Model] Add base class for vision-language models by @DarkLight1337 in https://github.com/vllm-project/vllm/pull/4809<br>[ROCm] Add support for Punica kernels on AMD GPUs by @kliuae in https://github.com/vllm-project/vllm/pull/3140<br>[Frontend] OpenAI API server: Do not add bos token by default when encoding by @bofenghuang in https://github.com/vllm-project/vllm/pull/4688 |

### 0.5.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.5.0](https://github.com/vllm-project/vllm/releases/tag/v0.5.0) | 2024-06-11 | Add OpenAI [Vision API](https://docs.vllm.ai/en/stable/models/vlm.html) support. Currently only LLaVA and LLaVA-NeXT are supported. We are working on …<br>[Kernel][ROCm][AMD] enable fused topk_softmax kernel for moe layer by @divakar-amd in https://github.com/vllm-project/vllm/pull/4927<br>Add OpenAI [Vision API](https://docs.vllm.ai/en/stable/models/vlm.html) support. Currently only LLaVA and LLaVA-NeXT are supported. We are working on … |
| [v0.5.0.post1](https://github.com/vllm-project/vllm/releases/tag/v0.5.0.post1) | 2024-06-14 | [Hardware][Intel] Optimize CPU backend and add more performance tips by @bigPYJ1151 in https://github.com/vllm-project/vllm/pull/4971<br>[CI/Build] Simplify OpenAI server setup in tests by @DarkLight1337 in https://github.com/vllm-project/vllm/pull/5100<br>[Bugfix] Fix typo in scheduler.py (requeset -> request) by @mgoin in https://github.com/vllm-project/vllm/pull/5470 |
| [v0.5.1](https://github.com/vllm-project/vllm/releases/tag/v0.5.1) | 2024-07-05 | [Model][Bugfix] Implicit model flags and reenable Phi-3-Vision by @DarkLight1337 in https://github.com/vllm-project/vllm/pull/5896<br>[Hardware][Intel] Optimize CPU backend and add more performance tips by @bigPYJ1151 in https://github.com/vllm-project/vllm/pull/4971<br>[Misc][Doc] Add Example of using OpenAI Server with VLM by @ywang96 in https://github.com/vllm-project/vllm/pull/5832 |
| [v0.5.2](https://github.com/vllm-project/vllm/releases/tag/v0.5.2) | 2024-07-15 | [Bugfix] Support 2D input shape in MoE layer by @WoosukKwon in https://github.com/vllm-project/vllm/pull/6287<br>[Bugfix][TPU] Add missing None to model input by @WoosukKwon in https://github.com/vllm-project/vllm/pull/6245<br>An experimental vLLM CLI for serving and querying OpenAI compatible server (#5090) |
| [v0.5.3](https://github.com/vllm-project/vllm/releases/tag/v0.5.3) | 2024-07-23 | In order to support long context, a new rope extension method has been added and chunked prefill has been turned on by default for Meta Llama 3.1 seri…<br>Many enhancements to TPU support. (#6277, #6457, #6506, #6504)<br>[Bugfix][CI/Build] Test prompt adapters in openai entrypoint tests by @g-eoj in https://github.com/vllm-project/vllm/pull/6419 |
| [v0.5.3.post1](https://github.com/vllm-project/vllm/releases/tag/v0.5.3.post1) | 2024-07-23 | [Bugfix] Fix a log error in chunked prefill by @WoosukKwon in https://github.com/vllm-project/vllm/pull/6694<br>[doc][distributed] fix doc argument order by @youkaichao in https://github.com/vllm-project/vllm/pull/6691 |
| [v0.5.4](https://github.com/vllm-project/vllm/releases/tag/v0.5.4) | 2024-08-05 | Enhanced vision language model support for InternVL2 (#6514, #7067), BLIP-2 (#5920), MiniCPM-V (#4087, #7122).<br>[Bugfix] Support cpu offloading with quant_method.process_weights_after_loading by @mgoin in https://github.com/vllm-project/vllm/pull/6960<br>[Bugfix] Add image placeholder for OpenAI Compatible Server of MiniCPM-V by @HwwwwwwwH in https://github.com/vllm-project/vllm/pull/6787 |
| [v0.5.5](https://github.com/vllm-project/vllm/releases/tag/v0.5.5) | 2024-08-23 | [Frontend][Core] Add plumbing to support audio language models by @petersalas in https://github.com/vllm-project/vllm/pull/7446<br>[misc] Add Torch profiler support for CPU-only devices by @DamonFool in https://github.com/vllm-project/vllm/pull/7806<br>[Feature]: Add OpenAI server prompt_logprobs support #6508 by @gnpinkert in https://github.com/vllm-project/vllm/pull/7453 |

### 0.6.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.6.0](https://github.com/vllm-project/vllm/releases/tag/v0.6.0) | 2024-09-04 | [Model] Add Ultravox support for multiple audio chunks by @petersalas in https://github.com/vllm-project/vllm/pull/7963<br>[Bugfix] neuron: enable tensor parallelism by @omrishiv in https://github.com/vllm-project/vllm/pull/7562<br>Add json_schema support from OpenAI protocol (#7654) |
| [v0.6.1](https://github.com/vllm-project/vllm/releases/tag/v0.6.1) | 2024-09-11 | [MISC] Keep chunked prefill enabled by default with long context when prefix caching is enabled by @comaniac in https://github.com/vllm-project/vllm/p…<br>[Hardware][Intel] Support compressed-tensor W8A8 for CPU backend by @bigPYJ1151 in https://github.com/vllm-project/vllm/pull/7257<br>Support load and unload LoRA in api server (#6566) |
| [v0.6.1.post1](https://github.com/vllm-project/vllm/releases/tag/v0.6.1.post1) | 2024-09-13 | [Hotfix][Core][VLM] Disable chunked prefill by default and prefix caching for multimodal models by @ywang96 in https://github.com/vllm-project/vllm/pu…<br>[Bugfix] multi-step + flashinfer: ensure cuda graph compatible  by @alexm-neuralmagic in https://github.com/vllm-project/vllm/pull/8427<br>[Hotfix][Core][VLM] Disable chunked prefill by default and prefix caching for multimodal models by @ywang96 in https://github.com/vllm-project/vllm/pu… |
| [v0.6.1.post2](https://github.com/vllm-project/vllm/releases/tag/v0.6.1.post2) | 2024-09-13 | [Doc] Add oneDNN installation to CPU backend documentation by @Isotr0py in https://github.com/vllm-project/vllm/pull/8467<br>[Misc] Skip loading extra bias for Qwen2-VL GPTQ-Int8 by @jeejeelee in https://github.com/vllm-project/vllm/pull/8442<br>[misc][ci] fix quant test by @youkaichao in https://github.com/vllm-project/vllm/pull/8449 |
| [v0.6.2](https://github.com/vllm-project/vllm/releases/tag/v0.6.2) | 2024-09-25 | [Kernel] Enable 8-bit weights in Fused Marlin MoE by @ElizaWszola in https://github.com/vllm-project/vllm/pull/8032<br>CPU: Enable mrope and support Qwen2-VL on CPU backend (#8770)<br>Introduce `MQLLMEngine` for API Server, boost throughput 30% in single step and 7% in multistep (#8157, #8761, #8584) |
| [v0.6.3](https://github.com/vllm-project/vllm/releases/tag/v0.6.3) | 2024-10-14 | [Bugfix] Fixes for Phi3v and Ultravox Multimodal EmbeddingInputs Support by @hhzhang16 in https://github.com/vllm-project/vllm/pull/8979<br>Add on-device sampling support for Neuron (#8746)<br>Support tool calling for InternLM2.5 (#8405) |
| [v0.6.3.post1](https://github.com/vllm-project/vllm/releases/tag/v0.6.3.post1) | 2024-10-17 | Support VLM2Vec, the first multimodal embedding model in vLLM (#9303)<br>[Hardware][CPU] compressed-tensor INT8 W8A8 AZP support  by @bigPYJ1151 in https://github.com/vllm-project/vllm/pull/9344<br>[Misc] Consolidate example usage of OpenAI client for multimodal models by @ywang96 in https://github.com/vllm-project/vllm/pull/9412 |
| [v0.6.4](https://github.com/vllm-project/vllm/releases/tag/v0.6.4) | 2024-11-15 | [Model] Add Qwen2-Audio model support by @faychu in https://github.com/vllm-project/vllm/pull/9248<br>CPU: Add embedding models support for CPU backend (#10193)<br>[Model] tool calling support for ibm-granite/granite-20b-functioncalling by @wseaton in https://github.com/vllm-project/vllm/pull/8339 |
| [v0.6.4.post1](https://github.com/vllm-project/vllm/releases/tag/v0.6.4.post1) | 2024-11-15 | [Misc] Bump up test_fused_moe tolerance by @ElizaWszola in https://github.com/vllm-project/vllm/pull/10364<br>[Bugfix] Ensure special tokens are properly filtered out for guided structured output with MistralTokenizer by @gcalmettes in https://github.com/vllm-…<br>[Misc] Fix some help info of arg_utils to improve readability by @ShangmingCai in https://github.com/vllm-project/vllm/pull/10362 |
| [v0.6.5](https://github.com/vllm-project/vllm/releases/tag/v0.6.5) | 2024-12-17 | [Model] Add Support for Multimodal Granite Models by @alex-jw-brooks in https://github.com/vllm-project/vllm/pull/10291<br>Improved hardware enablement for AMD ROCm, ARM AARCH64, TPU prefix caching, XPU AWQ/GPTQ, and various CPU/Gaudi/HPU/NVIDIA enhancements (#10254, #9228…<br>[Frontend] Add OpenAI API support for input_audio by @kylehh in https://github.com/vllm-project/vllm/pull/11027 |
| [v0.6.6](https://github.com/vllm-project/vllm/releases/tag/v0.6.6) | 2024-12-27 | [Doc] Add video example to openai client for multimodal by @Isotr0py in https://github.com/vllm-project/vllm/pull/11521<br>[Bugfix][Build/CI] Fix sparse CUTLASS compilation on CUDA [12.0, 12.2) by @tlrmchlsmth in https://github.com/vllm-project/vllm/pull/11311<br>[Doc] Add video example to openai client for multimodal by @Isotr0py in https://github.com/vllm-project/vllm/pull/11521 |
| [v0.6.6.post1](https://github.com/vllm-project/vllm/releases/tag/v0.6.6.post1) | 2024-12-27 | Update openai_compatible_server.md by @robertgshaw2-neuralmagic in https://github.com/vllm-project/vllm/pull/11536<br>This release restore functionalities for other quantized MoEs, which was introduced as part of initial DeepSeek V3 support 🙇 .<br>[V1] Fix yapf by @WoosukKwon in https://github.com/vllm-project/vllm/pull/11538 |

### 0.7.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.7.0](https://github.com/vllm-project/vllm/releases/tag/v0.7.0) | 2025-01-27 | Any model that implements merged multi-modal processor and the `get_*_embeddings` methods according to [this guide](https://docs.vllm.ai/en/latest/con…<br>[Bugfix] Fix for ROCM compressed tensor support by @selalipop in https://github.com/vllm-project/vllm/pull/11561<br>[V1] Add `RayExecutor` support for `AsyncLLM` (api server) by @jikunshang in https://github.com/vllm-project/vllm/pull/11712 |
| [v0.7.1](https://github.com/vllm-project/vllm/releases/tag/v0.7.1) | 2025-02-01 | [Misc][MoE] add Deepseek-V3 moe tuning support by @divakar-amd in https://github.com/vllm-project/vllm/pull/12558<br>[ROCm][AMD][Model] llama 3.2 support upstreaming by @maleksan85 in https://github.com/vllm-project/vllm/pull/12421<br>Disable chunked prefill and/or prefix caching when MLA is enabled  by @simon-mo in https://github.com/vllm-project/vllm/pull/12642 |
| [v0.7.2](https://github.com/vllm-project/vllm/releases/tag/v0.7.2) | 2025-02-06 | Support Pixtral-Large HF by using llava multimodal_projector_bias config by @mgoin in https://github.com/vllm-project/vllm/pull/12710<br>Enable DeepSeek model on ROCm (#12662)<br>[Core][v1] Unify allocating slots in prefill and decode in KV cache manager by @ShawnD200 in https://github.com/vllm-project/vllm/pull/12608 |
| [v0.7.3](https://github.com/vllm-project/vllm/releases/tag/v0.7.3) | 2025-02-20 | Add `/v1/audio/transcriptions` OpenAI API endpoint (#12909)<br>Add intial ROCm support to V1 (#12790)<br>Add `/v1/audio/transcriptions` OpenAI API endpoint (#12909) |

### 0.8.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.8.0](https://github.com/vllm-project/vllm/releases/tag/v0.8.0) | 2025-03-18 | [Bugfix][IPEX] Add `VLLM_CPU_MOE_PREPACK` to allow disabling MoE prepack when CPU does not support it by @gau-nernst in https://github.com/vllm-projec…<br>[FEAT] [ROCm] [Embedding] Add encoder-only model support into ROCm Flash Attention to enable embedding models. by @tjtanaa in https://github.com/vllm-…<br>[V1] Add regex structured output support with xgrammar by @russellb in https://github.com/vllm-project/vllm/pull/14590 |
| [v0.8.1](https://github.com/vllm-project/vllm/releases/tag/v0.8.1) | 2025-03-19 | MI325 configs, fused_moe_kernel bugfix by @ekuznetsov139 in https://github.com/vllm-project/vllm/pull/14987<br>[V1] TPU - Fix CI/CD runner for V1 and remove V0 tests by @alexm-redhat in https://github.com/vllm-project/vllm/pull/14974<br>Refactor Structured Output for multiple backends (#14694) |
| [v0.8.2](https://github.com/vllm-project/vllm/releases/tag/v0.8.2) | 2025-03-23 | Enable CUDA graph support for llama 3.2 vision (#14917)<br>Enable CUDA graph support for llama 3.2 vision (#14917)<br>Support tool calling and reasoning parser (#14511) |
| [v0.8.3](https://github.com/vllm-project/vllm/releases/tag/v0.8.3) | 2025-04-06 | [Docs] Document v0 engine support in reasoning outputs by @gaocegege in https://github.com/vllm-project/vllm/pull/15739<br>Add custom allreduce support for ROCM (#14125)<br>Add Phi-4-mini function calling support (#14886) |
| [v0.8.4](https://github.com/vllm-project/vllm/releases/tag/v0.8.4) | 2025-04-14 | [Bug] [ROCm] Fix Llama 4 Enablement Bug on ROCm: V0 ROCmFlashAttentionImpl and Triton Fused MoE bugs by @tjtanaa in https://github.com/vllm-project/vl…<br>[Bugfix] fix use-ep bug to enable ep by dp/tp size > 1 by @zxfan-cpu in https://github.com/vllm-project/vllm/pull/16161<br>[V1][Structured Output] Add `supports_structured_output()` method to Platform by @shen-shanshan in https://github.com/vllm-project/vllm/pull/16148 |
| [v0.8.5](https://github.com/vllm-project/vllm/releases/tag/v0.8.5) | 2025-04-28 | Add expert_map support to Cutlass FP8 MOE (#16861)<br>[Performance][ROCm] Add skinny gemms for unquantized linear on ROCm by @charlifu in https://github.com/vllm-project/vllm/pull/15830<br>This release features important multi-modal bug fixes, day 0 support for Qwen3, and xgrammar's structure tag feature for tool calling. |
| [v0.8.5.post1](https://github.com/vllm-project/vllm/releases/tag/v0.8.5.post1) | 2025-05-02 | This post release contains two bug fix for memory leak and model accuracy<br>This post release contains two bug fix for memory leak and model accuracy |

### 0.9.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.9.0](https://github.com/vllm-project/vllm/releases/tag/v0.9.0) | 2025-05-15 | [Misc] support model prefix & add deepseek vl2 tiny fused moe config by @xsank in https://github.com/vllm-project/vllm/pull/17763<br>[Bugfix] Add half type support in reshape_and_cache_cpu_impl on x86 cpu platform by @zzzyq in https://github.com/vllm-project/vllm/pull/18430<br>[Misc] Add a Jinja template to support Mistral3 function calling by @chaunceyjiang in https://github.com/vllm-project/vllm/pull/17195 |
| [v0.9.0.1](https://github.com/vllm-project/vllm/releases/tag/v0.9.0.1) | 2025-05-30 | Release notes 未匹配到已配置能力关键词 |
| [v0.9.1](https://github.com/vllm-project/vllm/releases/tag/v0.9.1) | 2025-06-10 | FP4: Add compressed-tensors NVFP4 support (#18312), FP4 MoE kernel optimization (#19110)<br>POWER: Add IBM POWER11 Support to CPU Extension Detection (#19082)<br>[Frontend] enable custom logging for the uvicorn server (OpenAI API server) by @fpaupier in https://github.com/vllm-project/vllm/pull/18403 |
| [v0.9.2](https://github.com/vllm-project/vllm/releases/tag/v0.9.2) | 2025-07-07 | [Quantization] Add compressed-tensors NVFP4 MoE Support by @dsikka in https://github.com/vllm-project/vllm/pull/19990<br>[Feature][ROCm] Add full graph capture support for TritonAttentionBackend by @charlifu in https://github.com/vllm-project/vllm/pull/19158<br>[Docs] Note that alternative structured output backends are supported by @russellb in https://github.com/vllm-project/vllm/pull/19426 |

### 0.10.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.10.0](https://github.com/vllm-project/vllm/releases/tag/v0.10.0) | 2025-07-24 | [Quantization] Enable BNB support for more MoE models by @jeejeelee in https://github.com/vllm-project/vllm/pull/21100<br>[Feature][ROCm] Add full graph capture support for TritonAttentionBackend by @charlifu in https://github.com/vllm-project/vllm/pull/19158<br>OpenAI compatibility: Responses API implementation (#20504, #20975), image object support in llm.chat (#19635), tool calling with required choice and … |
| [v0.10.1](https://github.com/vllm-project/vllm/releases/tag/v0.10.1) | 2025-08-18 | **Parallelization and MoE optimizations**: Guided decoding throughput improvements (#21862), balanced expert sharding for MoE models (#21497), expande…<br>**Hardware compatibility and kernels**: ARM CPU build fixes for systems without BF16 support (#21848), Machete memory-bound performance improvements (…<br>**OpenAI API compatibility**: Unix domain socket support for local communication (#18097), improved error response format matching upstream specificat… |
| [v0.10.1.1](https://github.com/vllm-project/vllm/releases/tag/v0.10.1.1) | 2025-08-20 | This is a critical bugfix and security release: |
| [v0.10.2](https://github.com/vllm-project/vllm/releases/tag/v0.10.2) | 2025-09-13 | [Feature][gpt-oss] Add support for num_cached_tokens and num_reasoning_tokens tracking by @NagyGeorge in https://github.com/vllm-project/vllm/pull/234…<br>**Hybrid and Mamba model improvements**: Enabled full CUDA graphs by default for hybrid models (#22594), disabled prefix caching for hybrid/Mamba mode…<br>**aarch64 support**: This release features native support for aarch64 allowing usage of vLLM on GB200 platform. The docker image `vllm/vllm-openai` sh… |

### 0.11.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.11.0](https://github.com/vllm-project/vllm/releases/tag/v0.11.0) | 2025-10-02 | [fix]: add Arm 4bit fused moe support by @nikhil-arm in https://github.com/vllm-project/vllm/pull/23809<br>[KV offload][3/N] Add worker-side CPU support by @orozery in https://github.com/vllm-project/vllm/pull/21448<br>Improve output when failing json.loads() on structured output test by @dougbtv in https://github.com/vllm-project/vllm/pull/25483 |
| [v0.11.1](https://github.com/vllm-project/vllm/releases/tag/v0.11.1) | 2025-11-18 | [Hardware][AMD][Model] Add Triton MoE tuning support and optimized configs for Qwen3 omni for MI308X (@sammysun0711 #28373)<br>[Perf] Refactor cudagraph_support to enable full CUDA graphs for spec decoding with FlashInfer (@benchislett #28479)<br>[EP/DP][API Server] Enable DP-aware routing in OpenAI API requests (@Prowindy #24945) |
| [v0.11.2](https://github.com/vllm-project/vllm/releases/tag/v0.11.2) | 2025-11-20 | [NVIDIA] Guard SM100 CUTLASS MoE macro to SM100 builds v2 (https://github.com/vllm-project/vllm/pull/28938)<br>[BugFix] Fix false assertion with spec-decode=[2,4,..] and TP>2 (https://github.com/vllm-project/vllm/pull/29036)<br>This release includes 4 bug fixes on top of `v0.11.1`: |

### 0.12.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.12.0](https://github.com/vllm-project/vllm/releases/tag/v0.12.0) | 2025-12-03 | **EAGLE Speculative Decoding Improvements**: Multi-step CUDA graph support (#29559), DP>1 support (#26086), and multimodal support with Qwen3VL (#2959…<br>**EAGLE Speculative Decoding Improvements**: Multi-step CUDA graph support (#29559), DP>1 support (#26086), and multimodal support with Qwen3VL (#2959…<br>**Tool Calling**: |

### 0.13.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.13.0](https://github.com/vllm-project/vllm/releases/tag/v0.13.0) | 2025-12-19 | **Performance**: Fused blockwise quant RMS norm (#27883), MoE LoRA loading reduction (#30243), encoder cache optimization (#30475), CPU KV offloading …<br>**Whisper**: Major performance improvements - [V1 is now faster than V0](https://github.com/vllm-project/vllm/issues/24946#issuecomment-3680725754) (~…<br>**Whisper**: Major performance improvements - [V1 is now faster than V0](https://github.com/vllm-project/vllm/issues/24946#issuecomment-3680725754) (~… |

### 0.14.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.14.0](https://github.com/vllm-project/vllm/releases/tag/v0.14.0) | 2026-01-20 | Vision LoRA mm_processor_cache support (#31927)<br>Excludes some not-yet-supported configurations: pipeline parallel, CPU backend, non-MTP/Eagle spec decoding.<br>**Tool Calling:** |
| [v0.14.1](https://github.com/vllm-project/vllm/releases/tag/v0.14.1) | 2026-01-24 | This is a patch release on top of `v0.14.0` to address a few security and memory leak fixes.<br>This is a patch release on top of `v0.14.0` to address a few security and memory leak fixes. |

### 0.15.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.15.0](https://github.com/vllm-project/vllm/releases/tag/v0.15.0) | 2026-01-29 | **MoE performance**: 1.2-2% E2E throughput improvement via grouped topk kernel fusion (#32058), NVFP4 small-batch decoding improvement (#30885), faste…<br>**FP4 kernel optimization**: Up to 65% faster FP4 quantization on Blackwell (SM100F) using 256-bit loads, ~4% E2E throughput improvement (#32520).<br>**Structured output**: Outlines byte fallback handling fix (#31391). |
| [v0.15.1](https://github.com/vllm-project/vllm/releases/tag/v0.15.1) | 2026-02-04 | **RTX Blackwell (SM120)**: Fixed NVFP4 MoE kernel support for RTX Blackwell workstation GPUs. Previously, NVFP4 MoE models would fail to load on these…<br>v0.15.1 is a patch release with security fixes, RTX Blackwell GPU fixes support, and bug fixes.<br>Enabled Triton MoE backend for FP8 per-tensor dynamic quantization (#33300) |

### 0.16.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.16.0](https://github.com/vllm-project/vllm/releases/tag/v0.16.0) | 2026-02-25 | **NVIDIA**: FlashInfer TRTLLM BF16 MoE integration (#32954), SM100 INT4 W4A16 kernel (#32437), SM121 (DGX Spark) CUTLASS support (#33517), MNNVL proto…<br>Bugfixes: FP8 online quantization memory fix (#31914), asymmetric W4A16 (ConchLinear) for CT (#33200), DeepSeek V3.2 NVFP4 (#33932), LoRA FP8 (#33879)…<br>Speculative decoding: Unified Parallel Drafting (#32887), structured output support (#33374), penalty application in MRV2 (#33251), skip softmax for a… |

### 0.17.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.17.0](https://github.com/vllm-project/vllm/releases/tag/v0.17.0) | 2026-03-07 | **Qwen3.5 Model Family**: Full support for the **Qwen3.5** model family (#34110) featuring GDN (Gated Delta Networks), with FP8 quantization, MTP spec…<br>**CPU**: ARM BF16 cross-compilation (#33079), FP16 for s390x (#34116), KleidiAI INT8_W4A8 for all input dtypes (#34890), s390x vector intrinsics for a…<br>Structured output bugfix for completions (#35237). |
| [v0.17.1](https://github.com/vllm-project/vllm/releases/tag/v0.17.1) | 2026-03-11 | Fix/resupport nongated fused moe triton (#36412)<br>Re-enable EP for trtllm MoE FP8 backend (#36494)<br>Fix/resupport nongated fused moe triton (#36412) |

### 0.18.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.18.0](https://github.com/vllm-project/vllm/releases/tag/v0.18.0) | 2026-03-20 | **GPU-less Render Serving**: New `vllm launch render` command (#36166, #34551) enables GPU-less preprocessing and rendering, allowing separation of mu…<br>**AMD ROCm**: Sparse MLA CUDA graphs (#35719), MTP lens > 1 in Sparse MLA (#36681), MLA with nhead<16 + FP8 KV for TP=8 (#35850), RoPE+KV cache fusion…<br>**Responses API Streaming Tool Calls**: The OpenAI Responses API now supports tool/function calling with streaming (#29947). |
| [v0.18.1](https://github.com/vllm-project/vllm/releases/tag/v0.18.1) | 2026-03-31 | Disable monolithic TRTLLM MoE for Renormalize routing #37605<br>Fix DeepGemm E8M0 accuracy degradation for Qwen3.5 FP8 on Blackwell (#38083)<br>Change default SM100 MLA prefill backend back to TRT-LLM (#38562) |

### 0.19.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.19.0](https://github.com/vllm-project/vllm/releases/tag/v0.19.0) | 2026-04-03 | **Gemma 4 support**: Full Google Gemma 4 architecture support including MoE, multimodal, reasoning, and tool-use capabilities (#38826, #38847). Requir…<br>**CPU**: Enable tcmalloc by default (#37607), graceful degradation without tcmalloc/libiomp (#37561), 48.9% throughput improvement for pooling models …<br>**CPU**: Enable tcmalloc by default (#37607), graceful degradation without tcmalloc/libiomp (#37561), 48.9% throughput improvement for pooling models … |
| [v0.19.1](https://github.com/vllm-project/vllm/releases/tag/v0.19.1) | 2026-04-18 | [Gemma4] Support quantized MoE (#39045)<br>[Gemma4] Support quantized MoE (#39045)<br>This is a patch release on top of `v0.19.0` with Transformers v5.5.3 upgrade and bug fixes for Gemma4: |

### 0.20.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.20.0](https://github.com/vllm-project/vllm/releases/tag/v0.20.0) | 2026-04-27 | **OpenAI / Anthropic API**: `presence_penalty` / `frequency_penalty` on Responses API (#38613), Responses API streaming migrated to unified parser (#3…<br>**Performance**: Optimize batch invariant with fused rms norm — 2.1% E2E latency improvement (#40413); avoid `seq_lens_cpu` GPU→CPU sync (#40654); cac…<br>**OpenAI / Anthropic API**: `presence_penalty` / `frequency_penalty` on Responses API (#38613), Responses API streaming migrated to unified parser (#3… |
| [v0.20.1](https://github.com/vllm-project/vllm/releases/tag/v0.20.1) | 2026-05-04 | Fixed reasoning parser kwargs not being passed to structured output (#41199).<br>Fixed `max_num_batched_token` not being captured in CUDA graph (#40734).<br>Fixed reasoning parser kwargs not being passed to structured output (#41199). |
| [v0.20.2](https://github.com/vllm-project/vllm/releases/tag/v0.20.2) | 2026-05-10 | **gpt-oss MXFP4 + torch.compile**: Plumbed `hidden_dim_unpadded` through the `moe_forward` fake op so MXFP4 works under `torch.compile` on v0.20.x (#4…<br>**DeepSeek V4 sparse attention**: Re-enable the persistent topk path on Hopper and ensure the memset kernel runs at CUDA graph capture time regardless…<br>**DeepSeek V4 KV cache**: Fixed a "failure to allocate KV blocks" error in the V1 engine KV cache manager (#41282). |

### 0.21.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.21.0](https://github.com/vllm-project/vllm/releases/tag/v0.21.0) | 2026-05-15 | **AMD ROCm**: ROCm 7.2.2 (#41386), DBO (Dynamic Batch Optimization) (#34726), AITER Fused Allreduce+RMSNorm (#37646), Fused Shared Expert (FSE) for Qw…<br>**AMD ROCm**: ROCm 7.2.2 (#41386), DBO (Dynamic Batch Optimization) (#34726), AITER Fused Allreduce+RMSNorm (#37646), Fused Shared Expert (FSE) for Qw…<br>**OpenAI compatibility**: `system_fingerprint` field in responses (#40537), `prompt_embeds` content part support (#40720), `defer_loading` and `tool_r… |

### 0.22.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.22.0](https://github.com/vllm-project/vllm/releases/tag/v0.22.0) | 2026-05-29 | **Completions**: `thinking_token_budget` support (#42116) with inverted-condition fix (#41674); map `reasoning_effort` to `enable_thinking` (#43401).<br>**DeepSeek V4 maturity**: DeepSeek V4 received a major hardening pass this cycle — the model was reorganized into a dedicated `vllm/models/deepseek_v4…<br>Docker: non-root `vllm-openai` target (#40275), build `mooncake-transfer-engine` from source (#42114), AINIC & Thor NIC support (#40453); Python-only … |
| [v0.22.1](https://github.com/vllm-project/vllm/releases/tag/v0.22.1) | 2026-06-05 | Normalize **NIXL** KV-connector wheel installs so only the wheel matching the image's CUDA major is kept, fixing `ImportError: libcudart.so.12` when i…<br>v0.22.1 is a patch release on top of v0.22.0 with targeted bug fixes plus a couple of additions: new model support for JetBrains' Mellum v2, zentorch-…<br>Fix a deterministic hang in multi-node **Ray data-parallel** serving with `num_api_servers > 1` by excluding the Ray DP backend from the deferred (ker… |

### 0.23.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.23.0](https://github.com/vllm-project/vllm/releases/tag/v0.23.0) | 2026-06-15 | **DeepSeek-V4 matures across backends**: Following its introduction in v0.22.0, DeepSeek-V4 received another large hardening and optimization pass. It…<br>**AMD ROCm**: ROCm 7.2.3 (#43136), AITER v0.1.13.post1 (#44265), native W4A16 (#41394) and fused-MoE W4A16 HIP (#44075) kernels for RDNA3 (gfx1100), A…<br>**Anthropic Messages API**: Structured output and effort support (#42396), system-role messages inside the messages array (#44283). |

### 0.24.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.24.0](https://github.com/vllm-project/vllm/releases/tag/v0.24.0) | 2026-06-29 | **Model Runner V2 (MRv2) continues to expand**: MRv2 now **supports quantized models by default** (#44446), enables **GraniteMoE by default** (#45461)…<br>**DeepSeek-V4 keeps maturing**: Following its debut, DeepSeek-V4 received another large optimization pass — a FlashInfer sparse index cache (2–4% TTFT…<br>**OpenAI / Responses**: Real `/v1/embeddings` support for messages + `chat_template_kwargs` (#45173), multimodal token counts in `usage.prompt_tokens_… |

### 0.25.x

| 版本 | 日期 | 关键 Feature / 修复证据 |
|---|---:|---|
| [v0.25.0](https://github.com/vllm-project/vllm/releases/tag/v0.25.0) | 2026-07-11 | Kernels: Helion `fused_qk_norm_rope` (#44010) and `silu_and_mul_per_block_quant` (#43994), Triton MLA logits workspace (#46819), swap-AB optimization …<br>Kernels: Helion `fused_qk_norm_rope` (#44010) and `silu_and_mul_per_block_quant` (#43994), Triton MLA logits workspace (#46819), swap-AB optimization …<br>New models: LLaVA-OneVision-2 (#44785), Unlimited OCR (#46564) with a Triton R-SWA backend (#47102), MOSS-Transcribe-Diarize (#47729), openai/privacy-… |
| [v0.25.1](https://github.com/vllm-project/vllm/releases/tag/v0.25.1) | 2026-07-14 | **Guard mixed-dtype allreduce RMSNorm quant fusions** (#48330). The fused FlashInfer allreduce + RMSNorm + static-quantization patterns could match gr…<br>v0.25.1 is a patch release containing two targeted bug fixes on top of v0.25.0. |

## 关键 Feature 的首次与最近证据

| 能力 | 首次证据 | 最近证据 |
|---|---|---|
| 模型能力 | v0.2.5：[BugFix] Fix input positions for long context with sliding window | v0.25.0：Kernels: Helion `fused_qk_norm_rope` (#44010) and `silu_and_mul_per_block_quant` (#43994), |
| 硬件与后端 | v0.1.4：Optimizing CUDA kernels for paged attention and GELU. | v0.25.0：Kernels: Helion `fused_qk_norm_rope` (#44010) and `silu_and_mul_per_block_quant` (#43994), |
| 推理服务 API | v0.1.2：ChatCompletion endpoint in OpenAI demo server | v0.25.0：New models: LLaVA-OneVision-2 (#44785), Unlimited OCR (#46564) with a Triton R-SWA backend |
| 调度与并行 | v0.1.3：fixed tensor parallel is not defined by @MoeedDar in https://github.com/vllm-project/vllm/ | v0.25.0：Speculative decoding: universal spec decode for heterogeneous vocabularies (TLI) (#38174); |
| 量化与 KV Cache | v0.2.0：Initial support for AWQ (performance not optimized) | v0.25.1：**Guard mixed-dtype allreduce RMSNorm quant fusions** (#48330). The fused FlashInfer allre |
| 性能与资源效率 | v0.1.4：[OPTIMIZATION] Optimizes the single_query_cached_kv_attention kernel by @naed90 in https:/ | v0.25.0：Kernels: Helion `fused_qk_norm_rope` (#44010) and `silu_and_mul_per_block_quant` (#43994), |
| 稳定性与可观测性 | v0.1.1：[Bugfix] Fix a bug in RequestOutput.finished by @WoosukKwon in https://github.com/vllm-pro | v0.25.1：v0.25.1 is a patch release containing two targeted bug fixes on top of v0.25.0. |

## 自动化观察

- 在已采集的 release note 中，`vLLM` 有直接证据覆盖：模型能力, 硬件与后端, 推理服务 API, 调度与并行, 量化与 KV Cache, 性能与资源效率, 稳定性与可观测性。
- 此报告描述的是 Release 明确披露的能力演进；未出现的能力应视为“尚未采集到证据”，而不是“不支持”。
