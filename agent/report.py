from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os

def generate_report(data):
    """生成报告"""
    date = datetime.now().strftime("%Y-%m-%d")

    # 设置模板加载器
    template_dir = os.path.join(os.path.dirname(__file__), "../templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.md")

    # 渲染模板
    report_content = template.render(
        date=date,
        pypi_version=data.get("pypi_version"),
        github_version=data.get("github_version"),
        version_comparison=data.get("version_comparison", "无对比"),
        daily_commits=data.get("daily_commits", "无提交"),
        popular_issues=data.get("popular_issues", "无 Issues"),
        feature_updates=data.get("feature_updates", "无更新"),
        bug_fixes=data.get("bug_fixes", "无修复"),
        performance_improvements=data.get("performance_improvements", "无改进"),
    )

    # 保存报告
    report_dir = os.path.join(os.path.dirname(__file__), "../reports")
    report_path = os.path.join(report_dir, f"{date}.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Report generated: {report_path}")
    return report_path