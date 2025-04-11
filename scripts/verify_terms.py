#!/usr/bin/env python3
import yaml
import re
import json
import argparse
from pathlib import Path
from termcolor import colored

class TermChecker:
    def __init__(self):
        with open("scripts/TERMS_zh.yml", encoding='utf-8') as f:
            self.terms = yaml.safe_load(f) or {}
        self.issues = []

    def check_files(self):
        for zh_path in Path("source/zh").rglob("*"):
            if zh_path.is_file() and zh_path.suffix in [".md", ".html"]:
                content = zh_path.read_text(encoding='utf-8')
                self._check_untranlated_terms(content, zh_path)
                self._check_inconsistent_terms(content, zh_path)

    def _check_untranlated_terms(self, content, file_path):
        for en_term in self.terms:
            if re.search(rf'\b{en_term}\b', content, re.IGNORECASE):
                self.issues.append({
                    "type": "untranslated",
                    "term": en_term,
                    "file": str(file_path.relative_to("source/zh")),
                    "snippet": self._get_context(content, en_term)
                })

    def _check_inconsistent_terms(self, content, file_path):
        for en, zh in self.terms.items():
            variations = re.findall(rf'{zh}[^的]?', content)
            if len(set(variations)) > 1:
                self.issues.append({
                    "type": "inconsistent",
                    "term": zh,
                    "file": str(file_path.relative_to("source/zh")),
                    "variations": list(set(variations))
                })

    def _get_context(self, text, term, context_chars=30):
        match = re.search(rf'.{{0,{context_chars}}}\b{term}\b.{{0,{context_chars}}}', text, re.IGNORECASE)
        return match.group(0) if match else ""

    def run(self):
        self.check_files()
        return bool(self.issues)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci', action='store_true', help='JSON output for CI')
    args = parser.parse_args()

    checker = TermChecker()
    has_issues = checker.run()

    if args.ci:
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues": checker.issues,
            "term_count": len(checker.terms),
            "status": "failure" if has_issues else "success"
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if has_issues:
            print(colored("\nTerm Issues Found:", "red"))
            for issue in checker.issues:
                if issue['type'] == "untranslated":
                    print(f"  - Untranslated '{issue['term']}' in {issue['file']}")
                    print(f"    Context: {issue['snippet']}\n")
                else:
                    print(f"  - Inconsistent '{issue['term']}' in {issue['file']}")
                    print(f"    Variations: {', '.join(issue['variations'])}\n")
            sys.exit(1)
        else:
            print(colored("✅ All terms verified", "green"))
            sys.exit(0)