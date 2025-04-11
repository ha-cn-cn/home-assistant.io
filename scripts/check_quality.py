#!/usr/bin/env python3
from pathlib import Path
import re


def check_translations():
    errors = []
    for file in Path('docs').rglob('*.zh.md'):
        content = file.read_text(encoding='utf-8')

        # 检查未翻译的术语
        if re.search(r'\b(entity|integration|automation)\b', content, re.IGNORECASE):
            errors.append(f"未翻译术语存在于 {file}")

        # 检查损坏的代码块
        if '```' in content and not re.search(r'```.*?```', content, re.DOTALL):
            errors.append(f"损坏的代码块在 {file}")

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("✅ 所有翻译通过基础质量检查")


if __name__ == "__main__":
    check_translations()