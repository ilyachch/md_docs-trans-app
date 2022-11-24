from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from md_translate.settings import Settings

from md_translate import const
from md_translate.exceptions import ConfigurationError

TEST_PATH = 'tests/test_data/md_files_folder'


class TestSettings(TestCase):
    def setUp(self) -> None:
        self.config_file_path = Path('tests/test_data/config.json')
        self.current_path = Path().cwd()
        self.test_path = Path(TEST_PATH)
        self.api_key = 'API_KEY'
        self.service_name = const.TRANSLATION_SERVICE_YANDEX
        self.source_lang = 'en'
        self.target_lang = 'ru'

    @patch('md_translate.settings.get_cli_args')
    def test_common_launch(self, cli_args_mock):
        cli_args_mock.return_value = '-s {} -S {} -T {}'.format(
            self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)
        self.assertEqual(settings.replace, False)

    @patch('md_translate.settings.get_cli_args')
    def test_launch_with_replace(self, cli_args_mock):
        cli_args_mock.return_value = '-s {} -S {} -T {} -R'.format(
            self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)
        self.assertEqual(settings.replace, True)

    @patch('md_translate.settings.get_cli_args')
    def test_lauch_with_path(self, cli_args_mock):
        cli_args_mock.return_value = '{} -s {} -S {} -T {}'.format(
            self.test_path, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.test_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)
        self.assertEqual(settings.replace, False)

    @patch('md_translate.settings.get_cli_args')
    def test_lauch_with_file(self, cli_args_mock):
        cli_args_mock.return_value = '-c {}'.format(
            self.config_file_path
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, const.TRANSLATION_SERVICE_GOOGLE)
        self.assertEqual(settings.source_lang, 'ru')
        self.assertEqual(settings.target_lang, 'en')
        self.assertEqual(settings.replace, False)

    @patch('md_translate.settings.get_cli_args')
    def test_lauch_with_file_and_override(self, cli_args_mock):
        cli_args_mock.return_value = '-c {} -s {} -S {} -T {}'.format(
            self.config_file_path, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)
        self.assertEqual(settings.replace, False)

    @patch('md_translate.settings.get_cli_args')
    def test_settings_are_not_valid(self, cli_args_mock):
        cli_args_mock.return_value = '-T {}'.format(
            self.target_lang
        ).split(' ')
        settings = Settings()
        with self.assertRaises(ConfigurationError):
            settings.source_lang
