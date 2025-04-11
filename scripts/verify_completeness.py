#!/usr/bin/env python3
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from termcolor import colored


class TranslationValidator:
    def __init__(self):
        self.en_dir = Path("source")
        self.zh_dir = Path("source/zh")
        self.missing_files = []
        self.untranslated_sections = {}

    def check_file_coverage(self):
        """检查文件级完整性"""
        for en_path in self.en_dir.rglob("*"):
            if en_path.is_file() and en_path.suffix in [".md", ".html"]:
                rel_path = en_path.relative_to(self.en_dir)
                zh_path = self.zh_dir / rel_path

                if not zh_path.exists():
                    self.missing_files.append(str(rel_path))
                else:
                    self.check_content_completeness(en_path, zh_path)

    def check_content_completeness(self, en_path, zh_path):
        """检查内容级完整性"""
        en_content = en_path.read_text(encoding='utf-8')
        zh_content = zh_path.read_text(encoding='utf-8')

        en_clean = self._clean_content(en_content)
        zh_clean = self._clean_content(zh_content)

        if len(zh_clean) / len(en_clean) < 0.6:  # 中文通常比英文短
            self.untranslated_sections[str(en_path)] = {
                "ratio": round(len(zh_clean) / len(en_clean), 2),
                "en_sample": en_clean[:100] + "..." if len(en_clean) > 100 else en_clean,
                "zh_sample": zh_clean[:100] + "..." if len(zh_clean) > 100 else zh_clean
            }

    def _clean_content(self, text):
        """清理不需要比较的内容"""
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        return text.strip()

    def run(self, strict=False):
        self.check_file_coverage()
        issues_found = bool(self.missing_files or self.untranslated_sections)

        if strict and not issues_found:
            # 严格模式下额外检查
            pass

        return issues_found


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci', action='store_true', help='JSON output for CI')
    parser.add_argument('--strict', action='store_true', help='Enable strict checks')
    args = parser.parse_args()

    validator = TranslationValidator()
    has_issues = validator.run(args.strict)

    if args.ci:
        report = {
            "timestamp": datetime.now().isoformat(),
            "missing_files": validator.missing_files,
            "untranslated_sections": validator.untranslated_sections,
            "status": "failure" if has_issues else "success"
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if validator.missing_files:
            print(colored("\nMissing Files:", "red"))
            for f in validator.missing_files:
                print(f"  - {f}")

        if validator.untranslated_sections:
            print(colored("\nPossibly Untranslated Sections:", "yellow"))
            for file, info in validator.untranslated_sections.items():
                print(f"  - {file} (ratio: {info['ratio']})")
                print(f"    EN: {info['en_sample']}")
                print(f"    ZH: {info['zh_sample']}\n")

        if has_issues:
            print(colored("❌ Issues found", "red"))
            sys.exit(1)
        else:
            print(colored("✅ All checks passed", "green"))
            sys.exit(0)