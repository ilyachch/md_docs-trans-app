import json
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict

from md_translate import const
from md_translate.exceptions import ConfigurationError


def get_cli_args():
    return sys.argv[1:]


class Settings:
    APPLICATION_DESCRIPTION = 'Translates .md files in folder'
    APPLICATION_EPILOG = 'See README.md for more information.'

    TRANSLATOR_API_KEY_FILENAME = '.md_translate_api_key'
    CONFIG_FILENAME = '.md_translate_config.ini'

    TRANSLATOR_API_KEY_FILE_DEFAULT_PATH = Path.home().joinpath(
        TRANSLATOR_API_KEY_FILENAME
    )
    CONFIG_FILE_DEFAULT_PATH = Path.home().joinpath(CONFIG_FILENAME)

    def __init__(self):
        self.__args_parser = self.get_arg_parser()
        self.__params: Namespace = self.__args_parser.parse_args(get_cli_args())
        self.__config = self.__get_config_from_file()

    def __get_config_from_file(self) -> Dict[str, str]:
        config_file_path = self.__params.config_path or self.CONFIG_FILE_DEFAULT_PATH
        if config_file_path.exists():
            return json.loads(config_file_path.read_text())
        return {}

    @property
    def source_lang(self):
        return self.__params.source_lang or self.__config.get('source_lang')

    @property
    def target_lang(self):
        return self.__params.target_lang or self.__config.get('target_lang')

    @property
    def service_name(self):
        return self.__params.service or self.__config.get('service_name')

    @property
    def api_key(self):
        return self.__params.api_key or self.__config.get('api_key')

    @property
    def path(self):
        return self.__params.path

    def is_valid(self) -> bool:
        for param_name in ['source_lang', 'target_lang', 'service_name', 'api_key']:
            param_value = getattr(self, param_name)
            if not param_value:
                return False
        return True

    def validate(self) -> None:
        if not self.is_valid():
            raise ConfigurationError()

    def get_arg_parser(self):
        arg_parser = ArgumentParser(
            description=self.APPLICATION_DESCRIPTION, epilog=self.APPLICATION_EPILOG
        )

        arg_parser.add_argument(
            'path',
            help='Path to folder to process. If not set, uses current folder',
            nargs='?',
            default=Path.cwd(),
            type=Path,
        )

        arg_parser.add_argument(
            '-c', '--config_path', help='Path to config_file', type=Path
        )

        arg_parser.add_argument(
            '-k',
            '--api_key',
            help='API key to use Translation API',
            type=str,
        )

        arg_parser.add_argument(
            '-s', '--service', help='Translating service',
            choices=(const.TRANSLATION_SERVICE_YANDEX, const.TRANSLATION_SERVICE_GOOGLE),
            type=str
        )
        arg_parser.add_argument(
            '-S', '--source_lang', help='Source language', choices=(const.LANG_EN, const.LANG_RU)
        )
        arg_parser.add_argument(
            '-T', '--target_lang', help='Target language', choices=(const.LANG_EN, const.LANG_RU)
        )
        return arg_parser


settings = Settings()
