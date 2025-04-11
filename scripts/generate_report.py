#!/usr/bin/env python3
from pathlib import Path
import markdown2
from datetime import datetime


def generate_html_report():
    """生成HTML格式的报告"""
    css = """
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        h1 { color: #333; }
        .issue { padding: 10px; margin: 5px 0; border-radius: 3px; }
        .missing { background-color: #ffeeee; border-left: 4px solid #ff4444; }
        .untranslated { background-color: #ffffdd; border-left: 4px solid #ffcc00; }
        .term { background-color: #eeffff; border-left: 4px solid #00dddd; }
        .success { color: #00aa00; }
    </style>
    """

    content = ["<h1>Translation Validation Report</h1>"]
    content.append(f"<p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>")

    # 收集各检查结果
    reports = {
        "completeness": Path("report.md").read_text(encoding='utf-8') if Path("report.md").exists() else "",
        "terms": Path("term_issues.txt").read_text(encoding='utf-8') if Path("term_issues.txt").exists() else "",
        "structure": Path("structure_issues.txt").read_text(encoding='utf-8') if Path(
            "structure_issues.txt").exists() else ""
    }

    # 生成报告部分
    for name, text in reports.items():
        if text:
            content.append(f"<h2>{name.capitalize()} Issues</h2>")
            content.append(markdown2.markdown(text))
        else:
            content.append(f'<p class="success">✅ No {name} issues found</p>')

    # 保存HTML报告
    html = f"<html><head>{css}</head><body>{''.join(content)}</body></html>"
    Path("report.html").write_text(html, encoding='utf-8')


if __name__ == "__main__":
    generate_html_report()