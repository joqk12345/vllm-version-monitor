---
name: vllm-version-monitor
version: 0.1.0
description: 定期检测 vLLM 项目的版本变化、代码提交和热门 Issues/PR，并生成每日报告。
author: Your Name
tags: [vllm, version-monitoring, daily-report]

# 技能执行
---

## 功能说明

该技能用于自动检测 vLLM 项目的以下信息：

- **PyPI 版本变化**：检测 pip install vllm 的版本更新
- **GitHub 发布**：检测 GitHub Releases 页面的版本
- **代码提交**：检测每日 Commit 变化
- **热门 Issues**：检测热门 Issues 和 PR 的更新情况

## 使用方法

### 1. 手动运行

```bash
cd ~/.claude/skills/vllm-version-monitor/agent
python monitor.py
```

### 2. 使用 GitHub Actions

在你的仓库中创建 `.github/workflows/vllm-monitor.yml` 文件：

```yaml
name: vLLM Version Monitor

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
          pip install requests jinja2
      - name: Run monitor
        run: |
          cd ~/.claude/skills/vllm-version-monitor/agent
          python monitor.py
      - name: Commit and push changes
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add ~/.claude/skills/vllm-version-monitor/reports/*.md
          git commit -m "Update daily report"
          git push
```

## 报告位置

报告存储在 `~/.claude/skills/vllm-version-monitor/reports/` 目录下，文件名格式为 `YYYY-MM-DD.md`。

## 更新技能

```bash
cd ~/.claude/skills/vllm-version-monitor
git pull
```

## 技术依赖

- Python 3.8+
- requests：用于发送 HTTP 请求
- jinja2：用于渲染报告模板

可以使用以下命令安装依赖：

```bash
pip install requests jinja2
```