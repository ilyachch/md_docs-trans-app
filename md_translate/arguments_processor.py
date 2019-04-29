import argparse
import os
import pathlib

from md_translate.exceptions import NoApiKeyFileError


class ArgumentsProcessor:
    APPLICATION_DESCRIPTION = 'Application allows to translate markdown files.\n' \
                              'See README.md for more information'

    TRANSLATOR_API_KEY_FILENAME = '.md_translate_api_key'

    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(self.APPLICATION_DESCRIPTION)
        self.parser = self.process_arguments()
        self.path = self.parser.path
        self.api_key = self.parser.api_key
        self.service = self.parser.service
        self.source_lang = self.parser.source_lang
        self.target_lang = self.parser.target_lang

    @property
    def api_key_value(self):
        with open(self.api_key) as api_key_file:
            return api_key_file.read()

    def process_arguments(self):
        self.arg_parser.add_argument(
            'path',
            help='Path to folder to process.',
            type=pathlib.Path)
        self.arg_parser.add_argument(
            '-k', '--api_key',
            help='Path to Translation Service API key file',
            default=os.path.join(str(pathlib.Path.home()), self.TRANSLATOR_API_KEY_FILENAME),
            type=pathlib.Path)
        self.arg_parser.add_argument(
            '-s', '--service',
            help='Translating service',
            default='Yandex', choices=('Yandex',)
        )
        self.arg_parser.add_argument(
            '-S', '--source_lang',
            help='Source language',
            default='en'
        )
        self.arg_parser.add_argument(
            '-T', '--target_lang',
            help='Target language',
            default='ru'
        )
        return self.arg_parser.parse_args()

    def validate_arguments(self):
        if not os.path.exists(self.api_key):
            raise NoApiKeyFileError


settings = ArgumentsProcessor()
