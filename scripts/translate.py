#!/usr/bin/env python3
import os
import re
import json
import yaml
import requests
from pathlib import Path
from datetime import datetime

CONFIG = {
    "source_dir": "source",
    "target_dir": "source/zh",
    "term_list": "docs/TERMS_zh.yml",
    "exclude_dirs": ["_data", "_includes", "assets"],
    "microsoft_api": {
        "endpoint": "https://api.cognitive.microsofttranslator.com/translate",
        "location": "global",
        "key": "",  # 留空使用免费版
        "free_auth_url": "https://edge.microsoft.com/translate/auth"
    }
}


class Translator:
    def __init__(self):
        self.terms = self.load_terms()
        self.auth_token = self.get_microsoft_token()

    def load_terms(self):
        try:
            with open(CONFIG["term_list"], encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}

    def get_microsoft_token(self):
        """获取免费的Microsoft翻译token"""
        try:
            response = requests.get(CONFIG["microsoft_api"]["free_auth_url"])
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"获取Microsoft token失败: {e}")
            return None

    def microsoft_translate(self, text, from_lang='en', to_lang='zh-Hans'):
        """使用Microsoft翻译API"""
        if not self.auth_token:
            return None

        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_lang
        }

        try:
            body = [{'text': text}]
            response = requests.post(
                CONFIG["microsoft_api"]["endpoint"],
                headers=headers,
                json=body,
                params=params
            )
            response.raise_for_status()
            return response.json()[0]['translations'][0]['text']
        except Exception as e:
            print(f"Microsoft翻译失败: {e}")
            return None

    def translate_text(self, text):
        """翻译文本（优先术语替换，其次API）"""
        # 先进行术语替换
        for en, zh in self.terms.items():
            text = re.sub(rf'\b{en}\b', zh, text, flags=re.IGNORECASE)

        # 尝试API翻译（只翻译长段落）
        if len(text) > 20 and self.auth_token:
            translated = self.microsoft_translate(text)
            if translated:
                return translated
        return text

    def translate_file(self, file_path):
        """翻译单个文件"""
        zh_path = Path(CONFIG["target_dir"]) / file_path.relative_to(CONFIG["source_dir"])
        zh_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 处理front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            front_matter = yaml.safe_load(parts[1]) or {}
            front_matter.update({
                "translation": True,
                "last_updated": datetime.now().strftime('%Y-%m-%d')
            })
            translated = f"---\n{yaml.dump(front_matter, allow_unicode=True)}---\n"
            body = parts[2] if len(parts) > 2 else ""
        else:
            translated = ""
            body = content

        # 分段落处理
        paragraphs = re.split(r'\n\n+', body)
        for para in paragraphs:
            if para.strip() and not para.startswith(('```', '<!--')):
                translated += self.translate_text(para) + "\n\n"
            else:
                translated += para + "\n\n"

        with open(zh_path, 'w', encoding='utf-8') as f:
            f.write(translated.strip())


def main():
    translator = Translator()

    # 只处理新增或修改的文件
    for en_file in Path(CONFIG["source_dir"]).rglob('*.md'):
        if any(ex in str(en_file) for ex in CONFIG["exclude_dirs"]):
            continue

        zh_file = Path(CONFIG["target_dir"]) / en_file.relative_to(CONFIG["source_dir"])
        if not zh_file.exists():
            print(f"Translating {en_file}")
            translator.translate_file(en_file)


if __name__ == "__main__":
    main()