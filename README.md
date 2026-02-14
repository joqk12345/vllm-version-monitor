# vLLM 版本监控技能

这是一个 Claude Code 技能，用于定期检测 vLLM 项目的版本变化、代码提交和热门 Issues/PR，并生成每日报告。

## 安装

```bash
cd ~/.claude/skills/
git clone [你的仓库地址] vllm-version-monitor
cd vllm-version-monitor
pip install -r requirements.txt
```

## 使用方法

### 1. 手动运行

```bash
cd ~/.claude/skills/vllm-version-monitor/agent
python monitor.py
```

### 2. 使用 GitHub Actions

参考 SKILL.md 文件中的说明。

## 报告存储

报告将保存在 `reports/` 目录下，每个报告文件以日期命名。

## 技术栈

- Python 3.8+
- requests
- jinja2

## 贡献

欢迎提交 PR 和 Issues！