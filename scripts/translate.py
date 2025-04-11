#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

CONFIG = {
    "content_dirs": ["docs", "src/content"],  # 需要翻译的目录
    "exclude_dirs": ["node_modules", "assets"],  # 排除目录
    "term_list": "scripts/TERMS_zh.yml",  # 术语表位置
    "file_types": [".md", ".html"],  # 需要翻译的文件类型
    "translation_suffix": ".zh"  # 翻译文件后缀
}


class CurrentRepoTranslator:
    def __init__(self):
        self.terms = self.load_terms()

    def load_terms(self):
        try:
            with open(CONFIG["term_list"], encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"术语表 {CONFIG['term_list']} 未找到，将继续不使用术语替换")
            return {}

    def should_translate(self, file_path):
        """判断文件是否需要翻译"""
        # 跳过已翻译文件
        if str(file_path).endswith(CONFIG["translation_suffix"] + file_path.suffix):
            return False

        # 跳过排除目录
        if any(ex_dir in str(file_path) for ex_dir in CONFIG["exclude_dirs"]):
            return False

        # 只处理指定类型文件
        return file_path.suffix.lower() in CONFIG["file_types"]

    def translate_content(self, text):
        """翻译内容（实际替换为你的翻译逻辑）"""
        # 术语替换
        for en, zh in self.terms.items():
            text = re.sub(rf'\b{en}\b', zh, text, flags=re.IGNORECASE)

        # 这里可以添加其他翻译逻辑
        # 例如调用免费翻译API或规则替换

        return text

    def process_file(self, file_path):
        """处理单个文件"""
        # 生成翻译文件名
        trans_path = file_path.with_name(
            f"{file_path.stem}{CONFIG['translation_suffix']}{file_path.suffix}"
        )

        print(f"正在处理: {file_path} -> {trans_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 处理front matter（如Markdown文件）
        if content.startswith('---'):
            parts = content.split('---', 2)
            front_matter = yaml.safe_load(parts[1]) or {}
            front_matter.update({
                "translation": True,
                "original_file": str(file_path),
                "last_updated": datetime.now().strftime('%Y-%m-%d')
            })
            translated = f"---\n{yaml.dump(front_matter, allow_unicode=True)}---\n"
            body = parts[2] if len(parts) > 2 else ""
        else:
            translated = ""
            body = content

        # 翻译正文内容
        translated += self.translate_content(body)

        # 写入翻译文件
        trans_path.parent.mkdir(parents=True, exist_ok=True)
        with open(trans_path, 'w', encoding='utf-8') as f:
            f.write(translated)

    def run(self):
        """主执行方法"""
        print("开始翻译当前仓库内容...")
        print(f"术语表加载: {len(self.terms)}条术语")

        for content_dir in CONFIG["content_dirs"]:
            if not Path(content_dir).exists():
                print(f"警告: 内容目录 {content_dir} 不存在")
                continue

            for file_path in Path(content_dir).rglob('*'):
                if file_path.is_file() and self.should_translate(file_path):
                    self.process_file(file_path)

        print("翻译完成")


if __name__ == "__main__":
    translator = CurrentRepoTranslator()
    translator.run()