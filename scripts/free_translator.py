#!/usr/bin/env python3
import os
import re
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup


class FreeTranslator:
    def __init__(self):
        self.terms = self.load_terms()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def load_terms(self):
        terms = {}
        term_file = Path('scripts/TERMS_zh.yml')
        if term_file.exists():
            with open(term_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        en, zh = line.split(':', 1)
                        terms[en.strip()] = zh.strip()
        return terms

    def get_microsoft_token(self):
        """获取免费的Microsoft翻译token"""
        try:
            r = self.session.get('https://edge.microsoft.com/translate/auth')
            r.raise_for_status()
            return r.text
        except Exception as e:
            print(f"获取Microsoft token失败: {e}")
            return None

    def translate_with_microsoft(self, text, src='en', dest='zh-Hans'):
        """使用Microsoft免费API翻译"""
        token = self.get_microsoft_token()
        if not token:
            return None

        try:
            url = 'https://api.cognitive.microsofttranslator.com/translate'
            params = {
                'api-version': '3.0',
                'from': src,
                'to': dest
            }
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            body = [{'text': text[:5000]}]  # 限制长度

            r = self.session.post(url, params=params, headers=headers, json=body)
            r.raise_for_status()
            return r.json()[0]['translations'][0]['text']
        except Exception as e:
            print(f"Microsoft翻译失败: {e}")
            return None

    def translate_with_libre(self, text):
        """备用方案：使用LibreTranslate（完全免费）"""
        try:
            # 使用公共实例（可能会限速）
            url = "https://libretranslate.de/translate"
            data = {
                'q': text[:2000],  # 更严格长度限制
                'source': 'en',
                'target': 'zh'
            }
            r = self.session.post(url, data=data)
            return r.json().get('translatedText')
        except:
            return None

    def translate_text(self, text):
        """综合翻译策略"""
        # 1. 术语替换
        for en, zh in self.terms.items():
            text = re.sub(rf'\b{en}\b', zh, text, flags=re.IGNORECASE)

        # 2. 尝试Microsoft免费API
        translated = self.translate_with_microsoft(text)
        if translated:
            return translated

        # 3. 备用方案：LibreTranslate
        translated = self.translate_with_libre(text)
        if translated:
            return translated

        # 4. 最终回退：保留原文
        return text

    def process_file(self, file_path):
        """处理单个文件"""
        zh_path = file_path.with_name(f"{file_path.stem}.zh{file_path.suffix}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取需要翻译的部分（跳过代码块）
        soup = BeautifulSoup(content, 'html.parser')
        for element in soup.find_all(text=True):
            if element.parent.name not in ['code', 'pre']:
                element.replace_with(self.translate_text(str(element)))

        zh_path.write_text(str(soup), encoding='utf-8')
        time.sleep(1)  # 避免速率限制

    def run(self):
        print("Starting free translation...")
        for file in Path('docs').rglob('*.md'):
            if '.zh.md' not in str(file):
                print(f"Translating {file}")
                self.process_file(file)


if __name__ == "__main__":
    FreeTranslator().run()