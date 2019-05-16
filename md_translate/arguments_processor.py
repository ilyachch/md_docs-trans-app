import configparser
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Union

from md_translate.exceptions import NoApiKeyFileError, NoConfigFileError, ConfigurationError


class ArgumentsProcessor:
    APPLICATION_DESCRIPTION = 'Translates .md files in folder'
    APPLICATION_EPILOG = 'See README.md for more information.'

    TRANSLATOR_API_KEY_FILENAME = '.md_translate_api_key'
    CONFIG_FILENAME = '.md_translate_config.ini'

    TRANSLATOR_API_KEY_FILE_DEFAULT_PATH = Path.home().joinpath(TRANSLATOR_API_KEY_FILENAME)
    CONFIG_FILE_DEFAULT_PATH = Path.home().joinpath(CONFIG_FILENAME)

    def __init__(self, args: list = sys.argv[1:]):
        self.args: list = args
        self.args_parser: ArgumentParser = self.__get_args_parser()
        self.params: Namespace = self.args_parser.parse_args(self.args)
        self.use_config_file = True
        self.config_file_path = self.CONFIG_FILE_DEFAULT_PATH

        self.path: Union[Path, None] = None
        self.api_key_file_path: Path = self.TRANSLATOR_API_KEY_FILE_DEFAULT_PATH
        self.api_key: Union[str, None] = None
        self.service: Union[str, None] = None
        self.source_lang: Union[str, None] = None
        self.target_lang: Union[str, None] = None

        self.set_settings()

    def __get_args_parser(self) -> ArgumentParser:
        arg_parser = ArgumentParser(
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
            type=str)

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
        if self.params.config_path is not None and self.params.config_path.exists():
            self.__set_settings_from_config_file(self.params.config_path)
        elif self.CONFIG_FILE_DEFAULT_PATH.exists():
            self.__set_settings_from_config_file(self.CONFIG_FILE_DEFAULT_PATH)

        self.path = self.params.path

        if self.params.api_key_file is not None:
            with self.params.api_key_file.open() as api_key_file:
                self.api_key = api_key_file.read()
        elif self.params.api_key is not None:
            self.api_key = self.params.api_key

        if self.params.api_key_file is None and self.params.api_key is None and self.api_key is None:
            if self.TRANSLATOR_API_KEY_FILE_DEFAULT_PATH.exists():
                with self.TRANSLATOR_API_KEY_FILE_DEFAULT_PATH.open() as api_key_file:
                    self.api_key = api_key_file.read()

        if self.params.service is not None:
            self.service = self.params.service

        if self.params.source_lang is not None:
            self.source_lang = self.params.source_lang

        if self.params.target_lang is not None:
            self.target_lang = self.params.target_lang

    def validate_arguments(self):
        settings_props = [self.service, self.source_lang, self.target_lang, self.api_key]
        if not all(settings_props):
            if self.CONFIG_FILE_DEFAULT_PATH.exists():
                raise ConfigurationError()
            elif not self.CONFIG_FILE_DEFAULT_PATH.exists():
                raise NoConfigFileError(self.CONFIG_FILE_DEFAULT_PATH)
        if self.params.api_key_file is not None and not self.params.api_key_file.exists():
            raise NoApiKeyFileError(self.params.api_key)

    def __set_settings_from_config_file(self, config_file_path: Path):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        config_ns = config['Settings']

        self.api_key = config_ns.get('api_key', None)
        self.service = config_ns.get('service', None)
        self.source_lang = config_ns.get('source_lang', None)
        self.target_lang = config_ns.get('target_lang', None)
