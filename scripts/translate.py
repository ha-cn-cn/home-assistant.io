import os
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import markdown
import frontmatter
from tqdm import tqdm
from datetime import datetime

# 配置
SOURCE_DIR = "source-en/source"
TARGET_DIR = "source-cn/source"
CACHE_FILE = "translation_cache.json"
GLOSSARY_FILE = "scripts/glossary.json"
EXCLUDE_DIRS = ["_includes", "_layouts", "_data"]
MAX_RETRIES = 3
DELAY_SECONDS = 1  # API请求之间的延迟


class Translator:
    def __init__(self):
        self.cache = self.load_cache()
        self.glossary = self.load_glossary()

    def load_cache(self):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_glossary(self):
        try:
            with open(GLOSSARY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_cache(self):
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def get_auth_token(self):
        url = "https://edge.microsoft.com/translate/auth"
        response = requests.get(url)
        return response.text

    def translate_text(self, text, from_lang="en", to_lang="zh-Hans"):
        # 检查缓存
        cache_key = f"{from_lang}-{to_lang}:{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 应用术语表替换
        for term, translation in self.glossary.items():
            text = text.replace(term, translation)

        # 如果已经在术语表中完全匹配，直接返回
        if text in self.glossary.values():
            self.cache[cache_key] = text
            return text

        # 调用微软翻译API
        token = self.get_auth_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        params = {
            "api-version": "3.0",
            "from": from_lang,
            "to": to_lang
        }

        body = [{"text": text}]

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    "https://api.cognitive.microsofttranslator.com/translate",
                    params=params,
                    headers=headers,
                    json=body
                )

                if response.status_code == 200:
                    translated = response.json()[0]['translations'][0]['text']
                    self.cache[cache_key] = translated
                    return translated
                else:
                    print(f"翻译失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {response.text}")
                    time.sleep(DELAY_SECONDS * (attempt + 1))

            except Exception as e:
                print(f"请求异常 (尝试 {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                time.sleep(DELAY_SECONDS * (attempt + 1))

        # 所有尝试都失败，返回原文
        return text

    def translate_markdown(self, content):
        # 解析frontmatter
        post = frontmatter.loads(content)

        # 翻译标题和描述（如果存在）
        if 'title' in post.metadata:
            post.metadata['title'] = self.translate_text(post.metadata['title'])

        if 'description' in post.metadata:
            post.metadata['description'] = self.translate_text(post.metadata['description'])

        # 翻译正文内容
        html = markdown.markdown(post.content)
        soup = BeautifulSoup(html, 'html.parser')

        # 提取所有需要翻译的文本节点
        text_nodes = []
        for element in soup.find_all(text=True):
            if element.parent.name not in ['code', 'pre', 'script', 'style']:
                if element.strip():
                    text_nodes.append(element)

        # 批量翻译（减少API调用）
        translations = {}
        for node in text_nodes:
            text = node.string
            if text and text.strip() and text not in translations:
                translations[text] = None

        # 执行翻译
        for text in translations:
            translations[text] = self.translate_text(text)

        # 应用翻译
        for node in text_nodes:
            if node.string in translations:
                node.string.replace_with(translations[node.string])

        # 重新构建Markdown
        translated_content = str(soup)
        post.content = translated_content

        return frontmatter.dumps(post)


def should_translate_file(path):
    # 排除非Markdown文件
    if not path.endswith('.md') and not path.endswith('.markdown'):
        return False

    # 排除特定目录
    for exclude_dir in EXCLUDE_DIRS:
        if f"/{exclude_dir}/" in path.replace("\\", "/"):
            return False

    return True


def sync_non_markdown_files():
    print("\n同步非Markdown文件...")
    for root, dirs, files in os.walk(SOURCE_DIR):
        # 跳过排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            src_path = os.path.join(root, file)
            if not should_translate_file(src_path):
                relative_path = os.path.relpath(src_path, SOURCE_DIR)
                dest_path = os.path.join(TARGET_DIR, relative_path)

                # 如果目标文件不存在或源文件较新，则复制
                if not os.path.exists(dest_path) or \
                        os.path.getmtime(src_path) > os.path.getmtime(dest_path):
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    print(f"复制: {relative_path}")
                    with open(src_path, 'rb') as src, open(dest_path, 'wb') as dest:
                        dest.write(src.read())


def main():
    print("Home Assistant 文档翻译系统启动")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    translator = Translator()
    processed_files = 0

    # 首先同步非Markdown文件
    sync_non_markdown_files()

    # 处理Markdown文件
    print("\n开始翻译Markdown文件...")
    md_files = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        # 跳过排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            src_path = os.path.join(root, file)
            if should_translate_file(src_path):
                md_files.append(src_path)

    # 使用进度条
    for src_path in tqdm(md_files, desc="翻译进度"):
        relative_path = os.path.relpath(src_path, SOURCE_DIR)
        dest_path = os.path.join(TARGET_DIR, relative_path)

        # 检查是否需要更新
        if os.path.exists(dest_path) and \
                os.path.getmtime(src_path) <= os.path.getmtime(dest_path):
            continue

        # 读取源文件
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 翻译内容
        translated_content = translator.translate_markdown(content)

        # 确保目标目录存在
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # 写入翻译后的文件
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        processed_files += 1

    # 保存缓存
    translator.save_cache()

    print(f"\n翻译完成！共处理 {processed_files} 个文件")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()