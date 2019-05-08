import argparse
import configparser
from pathlib import Path

from md_translate.exceptions import NoApiKeyFileError, NoConfigFileError


class ArgumentsProcessor:
    APPLICATION_DESCRIPTION = 'Application allows to translate markdown files.\n' \
                              'See README.md for more information.\n'

    TRANSLATOR_API_KEY_FILENAME = '.md_translate_api_key'
    CONFIG_FILENAME = '.md_translate_config.ini'

    TRANSLATOR_API_KEY_FILE_DEFAULT_PATH = Path.home().joinpath(TRANSLATOR_API_KEY_FILENAME)
    CONFIG_FILE_DEFAULT_PATH = Path.home().joinpath(CONFIG_FILENAME)

    def __init__(self):
        self.__arguments = self.process_arguments()

        self.path = None
        self.api_key = None
        self.service = None
        self.source_lang = None
        self.target_lang = None

        self.set_settings()

    @property
    def api_key_value(self):
        with open(self.api_key) as api_key_file:
            return api_key_file.read()

    def process_arguments(self):
        arg_parser = argparse.ArgumentParser(self.APPLICATION_DESCRIPTION)

        arg_parser.add_argument(
            'path',
            help='Path to folder to process. If not set, uses current folder',
            default=Path.cwd(),
            type=Path)
        arg_parser.add_argument(
            '-C', '--use_config',
            help='Use config file from default place (~/{})'.format(self.CONFIG_FILENAME),
            action='store_true',
        )
        arg_parser.add_argument(
            '-c', '--config_path',
            help='Path to config_file',
            type=Path
        )
        arg_parser.add_argument(
            '-k', '--api_key',
            help='Path to Translation Service API key file',
            default=self.TRANSLATOR_API_KEY_FILE_DEFAULT_PATH,
            type=Path)
        arg_parser.add_argument(
            '-s', '--service',
            help='Translating service',
            default='Yandex', choices=('Yandex', 'Google')
        )
        arg_parser.add_argument(
            '-S', '--source_lang',
            help='Source language',
            default='en'
        )
        arg_parser.add_argument(
            '-T', '--target_lang',
            help='Target language',
            default='ru'
        )
        return arg_parser.parse_args()

    def set_settings(self):
        if self.__arguments.use_config:
            if not self.CONFIG_FILE_DEFAULT_PATH.exists():
                raise NoConfigFileError
            else:
                self.__set_settings_from_config_file(self.CONFIG_FILE_DEFAULT_PATH)
        elif self.__arguments.config_path is not None:
            config_file_custom_path = Path(self.__arguments.config_path)
            if not config_file_custom_path.exists():
                raise NoConfigFileError
            else:
                self.__set_settings_from_config_file(config_file_custom_path)
        else:
            self.path = self.__arguments.path
            self.api_key = self.__arguments.api_key
            self.service = self.__arguments.service
            self.source_lang = self.__arguments.source_lang
            self.target_lang = self.__arguments.target_lang

    def validate_arguments(self):
        if not self.__arguments.api_key.exists():
            raise NoApiKeyFileError

    def __set_settings_from_config_file(self, config_file_path: Path):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        config_ns = config['Settings']

        self.api_key = config_ns['api_key']
        self.service = config_ns['service']
        self.source_lang = config_ns['source_lang']
        self.target_lang = config_ns['target_lang']


settings = ArgumentsProcessor()
