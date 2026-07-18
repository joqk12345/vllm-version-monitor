# Release Intelligence Reports

面向开源推理框架的可复现 Release Intelligence 管线。当前内置 **vLLM** 和 **SGLang**：从官方 GitHub Releases 拉取完整历史，规范化版本、提取 Feature 证据、生成详细分析与两页演进简报 PDF，并进行逐页视觉验证。

## 核心能力

- 官方 GitHub Releases 分页抓取、ETag 缓存、限流回退与离线重建。
- stable、post/patch、RC/prerelease 版本的语义化分类与排序。
- 基于 Release note 原文的确定性 Feature taxonomy；所有事实性条目保留来源 URL。
- 配置化的阶段演进模型：vLLM 六阶段、SGLang 五阶段。
- 每个项目输出两份 PDF：详细项目分析和严格两页的 Evolution Brief。
- `pdfinfo`、`pdftotext`、`pdftoppm`、PNG/contact sheet、SHA-256、JSON Schema 的完整验证链路。

## 前置条件

- Python 3.10+
- Poppler：`pdfinfo`、`pdftotext`、`pdftoppm`
- 可选：`GITHUB_TOKEN`，用于提升 GitHub API 限额；令牌不会写入缓存、报告或日志。

macOS 可使用：

```bash
brew install poppler
```

## 安装

```bash
python3 -m pip install -e '.[dev]'
```

## 一键构建

```bash
# vLLM
release-report build --config config/vllm.yaml

# SGLang
release-report build --config config/sglang.yaml
```

`build` 依次执行：`fetch → analyze → render → verify`。任一步失败都会返回非零退出码，且不会把未验证 PDF 当作成功产物。

也可使用：

```bash
make report
```

## CLI

```bash
release-report fetch --config config/vllm.yaml
release-report analyze --config config/vllm.yaml
release-report render --config config/vllm.yaml
release-report verify --config config/vllm.yaml
release-report build --config config/vllm.yaml
```

确定性离线重建：

```bash
release-report build \
  --config config/vllm.yaml \
  --cutoff 2026-07-18 \
  --offline
```

离线模式只读取 `data/raw/` 中的有效官方 API 缓存；没有缓存时会明确失败。

## 输出结构

每个项目使用独立输出根目录，避免不同项目覆盖 PDF、manifest 或 QA 文件：

```text
output/
├── vllm/
│   ├── pdf/
│   │   ├── vLLM_Project_Analysis_Version_Feature_Timeline.pdf
│   │   └── vLLM_Evolution_Brief.pdf
│   ├── json/
│   ├── qa/
│   └── build_manifest.json
└── sglang/
    ├── pdf/
    │   ├── SGLang_Project_Analysis_Version_Feature_Timeline.pdf
    │   └── SGLang_Evolution_Brief.pdf
    ├── json/
    ├── qa/
    └── build_manifest.json
```

`build_manifest.json` 记录项目、cutoff、数据来源模式、最新 stable 版本、所有主要 artifact 的大小和 SHA-256。`qa/verification.json` 记录 PDF 页数、页面尺寸、必需文本检查、渲染页和哈希。

需要保留同一机器上的多个构建时，传入 UTC 时间戳或任意安全 run identifier：

```bash
release-report build --config config/vllm.yaml --run-id 2026-07-18T11-30-00Z
```

产物将写入 `output/vllm/runs/2026-07-18T11-30-00Z/`。每日 GitHub Actions 自动生成该标识，并将完整 artifact 保留 365 天。

## 验证与测试

```bash
python3 -m pytest -q
release-report verify --config config/vllm.yaml --cutoff 2026-07-18 --offline
release-report verify --config config/sglang.yaml --cutoff 2026-07-18 --offline
```

验证会：

1. 读取 PDF 元数据和页数；
2. 检查必需标题、最新版本与来源说明；
3. 在 140 DPI 渲染每个 PDF 页面；
4. 生成 contact sheet；
5. 校验 `build_manifest.json`、`verification.json` 与其 JSON schemas；
6. 对 manifest 中的 artifact 校验 SHA-256 和文件大小。

## GitHub Actions

[`.github/workflows/vllm-monitor.yml`](.github/workflows/vllm-monitor.yml) 是每日工作流：安装依赖和 Poppler、运行测试、构建 vLLM 与 SGLang、验证 manifest，并上传 `output/` artifact。默认只读仓库内容，**不会自动推送提交或创建 Release**。

工作流传入 GitHub 内置 `GITHUB_TOKEN`；本地高频运行建议设置同名变量。

## 添加新项目

复制 `config/vllm.yaml`，修改：

- `owner`、`repository`、显示标题和输出目录；
- 官方文档链接与架构说明；
- stable/post/patch/RC 规则；
- Feature taxonomy；
- 版本阶段覆盖。

然后执行 `release-report build --config config/<project>.yaml`。渲染、缓存、manifest、schema 验证和 CLI 不需要重写。

## 已知边界

Feature 提取是以 Release note 段落和关键词为基础的确定性流程；它不会替代人工技术评估。没有官方证据的能力不得写成“支持”，需要标记为待确认。当前架构说明只使用配置的官方文档来源；历史 Release 与当前文档的语义差异应分别陈述。
