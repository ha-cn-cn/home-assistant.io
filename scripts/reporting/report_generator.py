#!/usr/bin/env python3
import json
import markdown
from jinja2 import Template
from pathlib import Path
from typing import List


class ReportGenerator:
    TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Translation Report</title>
    <style>
        .metric-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .progress-bar {
            height: 20px;
            background: #f0f0f0;
            border-radius: 4px;
        }
        .progress {
            height: 100%;
            border-radius: 4px;
            background: #4CAF50;
        }
    </style>
</head>
<body>
    <h1>Translation Quality Report</h1>

    {% for metric in metrics %}
    <div class="metric-card">
        <h2>{{ metric.name }}</h2>
        <div class="progress-bar">
            <div class="progress" style="width: {{ metric.percentage }}%"></div>
        </div>
        <p>{{ metric.value }} / {{ metric.total }} ({{ metric.percentage }}%)</p>

        {% if metric.details %}
        <h3>Issues:</h3>
        <ul>
            {% for item in metric.details %}
            <li>{{ item }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>"""

    def __init__(self, data_sources: List[str]):
        self.metrics = self._load_data(data_sources)

    def generate(self, output_dir: str, formats: List[str]):
        """生成多种格式报告"""
        Path(output_dir).mkdir(exist_ok=True)

        if 'html' in formats:
            self._generate_html(output_dir)
        if 'markdown' in formats:
            self._generate_markdown(output_dir)

    def _generate_html(self, output_dir: str):
        """生成HTML报告"""
        template = Template(self.TEMPLATE)
        html = template.render(metrics=self.metrics)
        (Path(output_dir) / 'report.html').write_text(html)

    def _generate_markdown(self, output_dir: str):
        """生成Markdown报告"""
        md_content = ["# Translation Quality Report\n"]
        for metric in self.metrics:
            md_content.append(
                f"## {metric['name']}\n"
                f"- **Score**: {metric['value']}/{metric['total']} ({metric['percentage']}%)\n"
            )
            if metric['details']:
                md_content.append("### Issues:\n" + "\n".join(f"- {item}" for item in metric['details']))

        (Path(output_dir) / 'report.md').write_text("\n".join(md_content))


if __name__ == "__main__":
    # 示例数据加载逻辑
    generator = ReportGenerator([
        'completeness.json',
        'term_validation.json'
    ])
    generator.generate('./reports', ['html', 'markdown'])