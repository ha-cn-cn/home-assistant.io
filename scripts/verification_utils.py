import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ContentAnalysis:
    code_ratio: float
    term_density: float
    link_count: int


class ContentAnalyzer:
    def analyze(self, file_path):
        """分析文件内容特征"""
        content = file_path.read_text(encoding='utf-8')

        # 计算代码占比
        code_blocks = re.findall(r'```.*?```', content, flags=re.DOTALL)
        code_len = sum(len(cb) for cb in code_blocks)
        code_ratio = code_len / len(content) if content else 0

        # 计算术语密度
        terms = re.findall(r'\b(entity|integration|automation)\b', content, re.I)
        term_density = len(terms) / (len(content.split()) + 1)

        # 计算链接数量
        links = re.findall(r'\[.*?\]\(.*?\)', content)

        return {
            'code_ratio': code_ratio,
            'term_density': term_density,
            'link_count': len(links),
            'segments': self._segment_content(content)
        }

    def _segment_content(self, content):
        """智能内容分段"""
        segments = []
        current_segment = ""
        in_code_block = False

        for line in content.split('\n'):
            if line.startswith('```'):
                if current_segment:
                    segments.append({
                        'type': 'text',
                        'content': current_segment
                    })
                    current_segment = ""
                in_code_block = not in_code_block
                segments.append({
                    'type': 'code',
                    'content': line
                })
            else:
                if in_code_block:
                    segments[-1]['content'] += '\n' + line
                else:
                    current_segment += '\n' + line

        if current_segment:
            segments.append({
                'type': 'text',
                'content': current_segment.strip()
            })

        return segments