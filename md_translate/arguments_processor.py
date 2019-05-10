import argparse
import configparser
from pathlib import Path

from md_translate.exceptions import NoApiKeyFileError, NoConfigFileError


class ArgumentsProcessor:
    APPLICATION_DESCRIPTION = 'Translates .md files in folder'
    APPLICATION_EPILOG = 'See README.md for more information.'

    TRANSLATOR_API_KEY_FILENAME = '.md_translate_api_key'
    CONFIG_FILENAME = '.md_translate_config.ini'

    TRANSLATOR_API_KEY_FILE_DEFAULT_PATH = Path.home().joinpath(TRANSLATOR_API_KEY_FILENAME)
    CONFIG_FILE_DEFAULT_PATH = Path.home().joinpath(CONFIG_FILENAME)

    def __init__(self):
        self.__args_parser = self.__get_args_parser()
        self.__arguments = self.__args_parser.parse_args()
        self.__use_config_file = True
        self.__config_file_path = self.CONFIG_FILE_DEFAULT_PATH

        self.path = None
        self.__api_key_file_path = self.TRANSLATOR_API_KEY_FILE_DEFAULT_PATH
        self.api_key = None
        self.service = None
        self.source_lang = None
        self.target_lang = None

        self.set_settings()

    def __get_args_parser(self) -> argparse.ArgumentParser:
        arg_parser = argparse.ArgumentParser(
            description=self.APPLICATION_DESCRIPTION,
            epilog=self.APPLICATION_EPILOG
        )

        arg_parser.add_argument(
            'path',
            help='Path to folder to process. If not set, uses current folder',
            nargs='?',
            default=Path.cwd(),
            type=Path)

        arg_parser.add_argument(
            '-c', '--config_path',
            help='Path to config_file',
            type=Path
        )

        api_key_group = arg_parser.add_mutually_exclusive_group()
        api_key_group.add_argument(
            '-k', '--api_key_file',
            help='Path to Translation Service API key file',
            type=Path)
        api_key_group.add_argument(
            '-K', '--api_key',
            help='API key to use Translation API',
            type=Path)

        arg_parser.add_argument(
            '-s', '--service',
            help='Translating service',
            choices=('Yandex', 'Google')
        )
        arg_parser.add_argument(
            '-S', '--source_lang',
            help='Source language',
        )
        arg_parser.add_argument(
            '-T', '--target_lang',
            help='Target language',
        )
        return arg_parser

    def set_settings(self):
        if self.__arguments.config_path is not None and self.__arguments.config_path.exists():
            self.__set_settings_from_config_file(self.__arguments.config_path)
        elif self.CONFIG_FILE_DEFAULT_PATH.exists():
            self.__set_settings_from_config_file(self.CONFIG_FILE_DEFAULT_PATH)

        self.path = self.__arguments.path

        if self.__arguments.api_key_file is not None:
            with self.__arguments.api_key_file.open() as api_key_file:
                self.api_key = api_key_file.read()
        elif self.__arguments.api_key is not None:
            self.api_key = self.__arguments.api_key

        if self.__arguments.service is not None:
            self.service = self.__arguments.service

        if self.__arguments.source_lang is not None:
            self.source_lang = self.__arguments.source_lang

        if self.__arguments.target_lang is not None:
            self.target_lang = self.__arguments.target_lang

    def validate_arguments(self):
        if self.__arguments.api_key_file is not None and not self.__arguments.api_key_file.exists():
            raise NoApiKeyFileError(self.__arguments.api_key)

    def __set_settings_from_config_file(self, config_file_path: Path):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        config_ns = config['Settings']

        self.api_key = config_ns['api_key']
        self.service = config_ns['service']
        self.source_lang = config_ns['source_lang']
        self.target_lang = config_ns['target_lang']


settings = ArgumentsProcessor()
