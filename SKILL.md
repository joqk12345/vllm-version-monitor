---
name: inference-framework-monitor
version: 0.2.0
description: 追踪 vLLM、SGLang、TensorRT-LLM 的版本、发布和开发活动，为能力对比建立历史数据。
author: Your Name
tags: [vllm, sglang, tensorrt-llm, version-monitoring]

# 技能执行
---

## 功能说明

该技能以 `config/projects.json` 为配置源，自动检测多个推理框架的以下信息：

- **PyPI 版本变化**：检测配置中声明的包版本
- **GitHub 发布**：检测每个项目的 GitHub Releases
- **代码提交**：按本地时区检测每日 Commit 变化
- **热门 Issues**：检测热门 Issues 和 PR 的更新情况
- **历史基线**：SQLite 保存本地完整快照；`agent/state.json` 保存 CI 可携带的比较游标
- **能力矩阵**：基于 `config/capabilities.json` 从 release note 提取带原始证据链接的 Feature 事件

本地高频运行时建议设置 `GITHUB_TOKEN`，避免 GitHub 匿名 API 限流；GitHub Actions 已自动传入 `github.token`。

## 使用方法

### 1. 手动运行

```bash
python3 agent/monitor.py
```

### 2. 使用 GitHub Actions

在你的仓库中创建 `.github/workflows/vllm-monitor.yml` 文件：

```yaml
name: Inference Framework Monitor

on:
  schedule:
    - cron: "0 0 * * *"  # 每天 UTC 时间 0 点运行

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run monitor
        run: |
          python3 agent/monitor.py
      - name: Commit and push changes
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add reports agent/state.json README.md CHANGELOG.md
          git diff --cached --quiet && exit 0
          git commit -m "chore: update framework monitor report"
          git push
```

## 报告位置

报告存储在 `reports/`，文件名格式为 `YYYY-MM-DD.md`。本地历史存储在 `data/monitor.db`，CI 比较游标存储在 `agent/state.json`。

## 更新技能

```bash
cd vllm-version-monitor
git pull
```

## 技术依赖

- Python 3.10+
- requests：用于发送 HTTP 请求

可以使用以下命令安装依赖：

```bash
python3 -m pip install -r requirements.txt
```
