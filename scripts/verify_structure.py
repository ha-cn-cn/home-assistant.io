#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
from datetime import datetime


class StructureValidator:
    def __init__(self):
        self.issues = []
        self.size_threshold = 0.3  # 默认阈值

    def compare_structure(self):
        en_files = {
            p.relative_to("source"): p.stat().st_size
            for p in Path("source").rglob("*")
            if p.is_file() and p.suffix in ['.md', '.html']
        }

        zh_files = {
            p.relative_to("source/zh"): p.stat().st_size
            for p in Path("source/zh").rglob("*")
            if p.is_file() and p.suffix in ['.md', '.html']
        }

        # 检查缺失文件
        for rel_path in set(en_files) - set(zh_files):
            self.issues.append({
                "type": "missing",
                "file": str(rel_path),
                "en_size": en_files[rel_path]
            })

        # 检查大小异常
        for rel_path in set(en_files) & set(zh_files):
            en_size = en_files[rel_path]
            zh_size = zh_files[rel_path]
            ratio = zh_size / en_size

            if not (self.size_threshold <= ratio <= 0.9):
                self.issues.append({
                    "type": "size_anomaly",
                    "file": str(rel_path),
                    "en_size": en_size,
                    "zh_size": zh_size,
                    "ratio": round(ratio, 2)
                })

    def run(self):
        self.compare_structure()
        return bool(self.issues)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci', action='store_true', help='JSON output for CI')
    parser.add_argument('--threshold', type=float, default=0.3,
                        help='Minimum size ratio (zh/en)')
    args = parser.parse_args()

    validator = StructureValidator()
    validator.size_threshold = args.threshold
    has_issues = validator.run()

    if args.ci:
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues": validator.issues,
            "threshold": args.threshold,
            "status": "failure" if has_issues else "success"
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if has_issues:
            print("Structure Issues Found:")
            for issue in validator.issues:
                if issue['type'] == "missing":
                    print(f"  - Missing: {issue['file']} (EN size: {issue['en_size']}b)")
                else:
                    print(f"  - Size anomaly: {issue['file']}")
                    print(f"    EN: {issue['en_size']}b  ZH: {issue['zh_size']}b")
                    print(f"    Ratio: {issue['ratio']} (threshold: {args.threshold})\n")
            sys.exit(1)
        else:
            print("✅ Structure validation passed")
            sys.exit(0)