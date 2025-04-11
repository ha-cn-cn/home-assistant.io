#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Dict, List

class CompletenessChecker:
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
        self.metrics = {
            'missing_files': [],
            'low_quality': [],
            'pass_count': 0
        }

    def check(self, source_dir: str, target_dir: str) -> Dict:
        """执行完整性检查"""
        source_files = self._scan_files(source_dir)
        target_files = self._scan_files(target_dir)

        for rel_path, src_info in source_files.items():
            if rel_path not in target_files:
                self.metrics['missing_files'].append({
                    'file': rel_path,
                    'size': src_info['size']
                })
            else:
                self._check_quality(rel_path, src_info, target_files[rel_path])

        return self.metrics

    def _scan_files(self, base_dir: str) -> Dict:
        """扫描目录结构"""
        files = {}
        for path in Path(base_dir).rglob('*'):
            if path.is_file() and path.suffix in ['.md', '.html']:
                rel_path = str(path.relative_to(base_dir))
                files[rel_path] = {
                    'size': path.stat().st_size,
                    'path': str(path)
                }
        return files

    def _check_quality(self, rel_path: str, src_info: Dict, tgt_info: Dict) -> bool:
        """检查翻译质量"""
        ratio = tgt_info['size'] / src_info['size']
        if ratio < self.threshold:
            self.metrics['low_quality'].append({
                'file': rel_path,
                'ratio': round(ratio, 2),
                'source_size': src_info['size'],
                'target_size': tgt_info['size']
            })
            return False
        self.metrics['pass_count'] += 1
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='source', help='Source directory')
    parser.add_argument('--target', default='source/zh', help='Target directory')
    parser.add_argument('--threshold', type=float, default=0.6)
    parser.add_argument('--ci', action='store_true', help='CI output mode')
    parser.add_argument('--strict', action='store_true', help='Enable strict mode')
    args = parser.parse_args()

    checker = CompletenessChecker(args.threshold)
    results = checker.check(args.source, args.target)

    if args.ci:
        print(json.dumps({
            'status': 'success' if not results['missing_files'] else 'failure',
            'metrics': results
        }, indent=2))
    else:
        if results['missing_files']:
            print(f"Missing files: {len(results['missing_files'])}")
        if results['low_quality']:
            print(f"Low quality translations: {len(results['low_quality'])}")
        print(f"Passed files: {results['pass_count']}")