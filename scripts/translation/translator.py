#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path
from term_manager import TermManager
from translation_engine import TranslationEngine


class Translator:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.term_manager = TermManager(self.config['term_blacklist'])
        self.engine = TranslationEngine(
            self.config['translation_engine'],
            retries=self.config.get('retries', 3)
        )

    def _load_config(self, config_path):
        """加载YAML配置文件"""
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def translate_file(self, file_path):
        """处理单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            translated = self.engine.translate(
                content,
                self.term_manager
            )
            output_path = self._get_output_path(file_path)
            output_path.write_text(translated, encoding='utf-8')
            return True
        except Exception as e:
            logging.error(f"Failed to translate {file_path}: {str(e)}")
            return False

    def _get_output_path(self, input_path):
        """生成输出路径"""
        rel_path = input_path.relative_to(self.config['source_dir'])
        return Path(self.config['output_dir']) / rel_path

    def run(self):
        """执行批量翻译"""
        success = 0
        total = 0

        for file in Path(self.config['source_dir']).rglob('*'):
            if self._should_process(file):
                total += 1
                if self.translate_file(file):
                    success += 1

        logging.info(f"Translation completed: {success}/{total} files")
        return success == total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--retries', type=int, default=3)
    args = parser.parse_args()

    translator = Translator(args.config)
    if not translator.run():
        raise SystemExit(1)