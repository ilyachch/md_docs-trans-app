import json
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, List

from md_translate import const
from md_translate.exceptions import ConfigurationError
from md_translate.utils import Singletone


def get_cli_args() -> List[str]:
    return sys.argv[1:]


class Settings(Singletone):
    APPLICATION_DESCRIPTION = 'Translates .md files in folder'
    APPLICATION_EPILOG = 'See README.md for more information.'

    TRANSLATOR_API_KEY_FILENAME = '.md_translate_api_key'
    CONFIG_FILENAME = '.md_translate_config.ini'

    TRANSLATOR_API_KEY_FILE_DEFAULT_PATH = Path.home().joinpath(
        TRANSLATOR_API_KEY_FILENAME
    )
    CONFIG_FILE_DEFAULT_PATH = Path.home().joinpath(CONFIG_FILENAME)

    def __init__(self) -> None:
        self.__args_parser = self.get_arg_parser()
        self.params: Namespace = self.__args_parser.parse_args(get_cli_args())
        self.config = self.__get_config_from_file()

    def __get_config_from_file(self) -> Dict[str, str]:
        config_file_path = self.params.config_path or self.CONFIG_FILE_DEFAULT_PATH
        if config_file_path.exists():
            return json.loads(config_file_path.read_text())
        return {}

    @property
    def source_lang(self) -> str:
        return self.__get_property_by_name('source_lang')

    @property
    def target_lang(self) -> str:
        return self.__get_property_by_name('target_lang')

    @property
    def service_name(self) -> str:
        return self.__get_property_by_name('service_name')

    @property
    def path(self) -> Path:
        return self.params.path

    def __get_property_by_name(self, prop_name: str) -> str:
        property_value = getattr(self.params, prop_name, None) or self.config.get(
            prop_name
        )
        if property_value is None:
            raise ConfigurationError(prop_name)
        return property_value

    def get_arg_parser(self) -> ArgumentParser:
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
            '-s',
            '--service',
            help='Translating service',
            choices=const.TRANSLATOR_BY_SERVICE_NAME.keys(),
            type=str,
            dest='service_name',
        )
        arg_parser.add_argument(
            '-S', '--source_lang', help='Source language code',
        )
        arg_parser.add_argument(
            '-T', '--target_lang', help='Target language code',
        )
        return arg_parser


settings = Settings()
