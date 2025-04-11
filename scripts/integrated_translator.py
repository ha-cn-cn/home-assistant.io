#!/usr/bin/env python3
import os
import re
import time
from pathlib import Path
from free_translator import FreeTranslator
from verification_utils import ContentAnalyzer


class IntegratedTranslator:
    def __init__(self):
        self.translator = FreeTranslator()
        self.analyzer = ContentAnalyzer()
        self.translation_log = []

    def process_file(self, file_path):
        """增强的翻译处理流程"""
        zh_path = file_path.with_name(f"{file_path.stem}.zh{file_path.suffix}")

        # 分析源文件复杂度
        analysis = self.analyzer.analyze(file_path)
        if analysis['code_ratio'] > 0.3:  # 代码占比高的文件特殊处理
            self._handle_technical_file(file_path, zh_path, analysis)
        else:
            self._handle_regular_file(file_path, zh_path)

        self.translation_log.append({
            'file': str(file_path),
            'status': 'translated',
            'analysis': analysis
        })

    def _handle_regular_file(self, en_path, zh_path):
        """处理普通文档"""
        content = en_path.read_text(encoding='utf-8')
        translated = self.translator.translate(content)
        zh_path.write_text(translated, encoding='utf-8')
        time.sleep(1)  # 遵守API速率限制

    def _handle_technical_file(self, en_path, zh_path, analysis):
        """处理技术文档（代码占比高）"""
        # 分段处理技术文档
        segments = self.analyzer.segment_file(en_path)
        translated_segments = []

        for seg in segments:
            if seg['type'] == 'code':
                translated_segments.append(seg['content'])
            else:
                translated = self.translator.translate(seg['content'])
                translated_segments.append(translated)

        zh_path.write_text('\n'.join(translated_segments), encoding='utf-8')

    def run(self):
        """执行整合流程"""
        print("🚀 Starting integrated translation")
        source_files = list(Path("docs").rglob("*"))

        for file in source_files:
            if self._should_translate(file):
                print(f"Processing {file.name}")
                self.process_file(file)

        self._generate_outputs()
        print("✅ Translation completed with verification")

    def _should_translate(self, file):
        """判断是否需要翻译"""
        conditions = [
            file.is_file(),
            file.suffix in ['.md', '.html'],
            '.zh.' not in str(file),
            not any(p in file.parts for p in ['node_modules', 'assets'])
        ]
        return all(conditions)

    def _generate_outputs(self):
        """生成GitHub Actions输出"""
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"file_count={len(self.translation_log)}\n")

        # 保存处理日志
        with open('translation_log.json', 'w') as f:
            json.dump(self.translation_log, f)


if __name__ == "__main__":
    IntegratedTranslator().run()