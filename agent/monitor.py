import requests
import json
from datetime import datetime
import os

def get_pypi_version():
    """获取 PyPI 上的 vLLM 最新版本"""
    url = "https://pypi.org/pypi/vllm/json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("info", {}).get("version")
    except Exception as e:
        print(f"Failed to get PyPI version: {e}")
        return None


def get_github_release_version():
    """获取 GitHub Releases 上的 vLLM 最新版本"""
    url = "https://api.github.com/repos/vllm-project/vllm/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("tag_name")
    except Exception as e:
        print(f"Failed to get GitHub release version: {e}")
        return None


def get_daily_commits(date):
    """获取指定日期的 Commits"""
    url = f"https://api.github.com/repos/vllm-project/vllm/commits?since={date}T00:00:00Z&until={date}T23:59:59Z"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Failed to get daily commits: {e}")
        return []


def get_popular_issues():
    """获取热门 Issues 和 PRs"""
    url = "https://api.github.com/repos/vllm-project/vllm/issues?sort=comments&per_page=5"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Failed to get popular issues: {e}")
        return []


def compare_versions(old_version, new_version):
    """比较版本"""
    if old_version and new_version and old_version != new_version:
        return f"从 {old_version} 更新到 {new_version}"
    elif old_version == new_version:
        return "版本无变化"
    else:
        return "无法比较版本"


def extract_commit_info(commits):
    """提取提交信息"""
    if not commits:
        return "无提交"

    commit_info = []
    for commit in commits:
        commit_date = commit.get("commit", {}).get("committer", {}).get("date")
        commit_date_formatted = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
        commit_info.append(
            f"- {commit.get('sha', 'No SHA')} - {commit.get('commit', {}).get('message', 'No message')} ({commit_date_formatted})"
        )
    return "\n".join(commit_info)


def extract_issue_info(issues):
    """提取 issue 信息"""
    if not issues:
        return "无热门 Issues"

    issue_info = []
    for issue in issues:
        issue_info.append(
            f"- #{issue.get('number')}: {issue.get('title', 'No title')} ({issue.get('comments', 0)} 条评论)"
        )
    return "\n".join(issue_info)


def monitor_all():
    """执行完整检测"""
    print("Starting vLLM version monitoring...")

    pypi_version = get_pypi_version()
    github_version = get_github_release_version()
    date = datetime.now().strftime("%Y-%m-%d")
    daily_commits = get_daily_commits(date)
    popular_issues = get_popular_issues()

    # 简单的版本对比（这里可以扩展为从历史数据中获取旧版本）
    version_comparison = compare_versions("0.0.0", github_version)
    commit_info = extract_commit_info(daily_commits)
    issue_info = extract_issue_info(popular_issues)

    print("Monitoring complete!")

    return {
        "pypi_version": pypi_version,
        "github_version": github_version,
        "version_comparison": version_comparison,
        "daily_commits": commit_info,
        "popular_issues": issue_info,
        "feature_updates": "待实现",
        "bug_fixes": "待实现",
        "performance_improvements": "待实现",
    }


from report import generate_report

if __name__ == "__main__":
    # 测试检测功能
    data = monitor_all()

    print("\n=== Test Results ===")
    print(f"PyPI Version: {data['pypi_version']}")
    print(f"GitHub Release: {data['github_version']}")
    print(f"Version Comparison: {data['version_comparison']}")
    print(f"\nDaily Commits:\n{data['daily_commits']}")
    print(f"\nPopular Issues:\n{data['popular_issues']}")

    # 生成报告
    report_path = generate_report(data)
    print(f"\nReport saved to: {report_path}")