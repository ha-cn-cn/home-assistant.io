#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime


def generate_html_report():
    """生成包含所有验证结果的HTML报告"""
    css = """
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        .issue { margin: 10px 0; padding: 10px; border-left: 4px solid; }
        .missing { border-color: #ff4444; background: #ffeeee; }
        .term { border-color: #ffcc00; background: #ffffdd; }
        .structure { border-color: #00aaff; background: #eeffff; }
        pre { background: #f5f5f5; padding: 10px; }
    </style>
    """

    report = [f"<h1>Translation Validation Report - {datetime.now().strftime('%Y-%m-%d')}</h1>"]

    # 1. 加载各检查结果
    results = {
        'completeness': json.loads(Path('completeness.json').read_text()) if Path(
            'completeness.json').exists() else None,
        'terms': json.loads(Path('terms.json').read_text()) if Path('terms.json').exists() else None,
        'structure': json.loads(Path('structure.json').read_text()) if Path('structure.json').exists() else None
    }

    # 2. 生成报告部分
    for check_type, data in results.items():
        if not data:
            continue

        report.append(f"<h2>{check_type.capitalize()} Issues</h2>")

        if data.get('status') == 'success':
            report.append("<p>✅ No issues found</p>")
            continue

        for issue in data.get('issues', []):
            if check_type == 'completeness':
                report.append(f"""
                <div class="issue missing">
                    <h3>Missing: {issue}</h3>
                </div>
                """)
            elif check_type == 'terms':
                report.append(f"""
                <div class="issue term">
                    <h3>{issue['type'].capitalize()} term: {issue['term']}</h3>
                    <p>File: {issue['file']}</p>
                    <pre>{issue.get('snippet', '')}</pre>
                </div>
                """)
            elif check_type == 'structure':
                report.append(f"""
                <div class="issue structure">
                    <h3>Size anomaly: {issue['file']}</h3>
                    <p>EN: {issue['en_size']}b → ZH: {issue['zh_size']}b (ratio: {issue['ratio']})</p>
                </div>
                """)

    # 3. 保存HTML文件
    html = f"<html><head>{css}</head><body>{''.join(report)}</body></html>"
    Path('report.html').write_text(html)
    Path('translation_issues.md').write_text("\n".join(
        f"- {k}: {len(v['issues'])} issues"
        for k, v in results.items()
        if v and v.get('issues')
    ))


if __name__ == "__main__":
    generate_html_report()