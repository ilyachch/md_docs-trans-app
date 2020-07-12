from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

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
        self.source_lang = const.LANG_EN
        self.target_lang = const.LANG_RU

    @patch('md_translate.settings.get_cli_args')
    def test_common_launch(self, cli_args_mock):
        from md_translate.settings import Settings
        cli_args_mock.return_value = '-k {} -s {} -S {} -T {}'.format(
            self.api_key, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.api_key, self.api_key)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)

    @patch('md_translate.settings.get_cli_args')
    def test_lauch_with_path(self, cli_args_mock):
        from md_translate.settings import Settings
        cli_args_mock.return_value = '{} -k {} -s {} -S {} -T {}'.format(
            self.test_path, self.api_key, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.test_path)
        self.assertEqual(settings.api_key, self.api_key)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)

    @patch('md_translate.settings.get_cli_args')
    def test_lauch_with_file(self, cli_args_mock):
        from md_translate.settings import Settings
        cli_args_mock.return_value = '-c {}'.format(
            self.config_file_path
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.api_key, 'API_KEY_IN_FILE')
        self.assertEqual(settings.service_name, const.TRANSLATION_SERVICE_GOOGLE)
        self.assertEqual(settings.source_lang, const.LANG_RU)
        self.assertEqual(settings.target_lang, const.LANG_EN)

    @patch('md_translate.settings.get_cli_args')
    def test_lauch_with_file_and_override(self, cli_args_mock):
        from md_translate.settings import Settings
        cli_args_mock.return_value = '-c {} -k {} -s {} -S {} -T {}'.format(
            self.config_file_path, self.api_key, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.api_key, self.api_key)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)

    @patch('md_translate.settings.get_cli_args')
    def test_settings_are_not_valid(self, cli_args_mock):
        from md_translate.settings import Settings
        cli_args_mock.return_value = '-k {} -T {}'.format(
            self.api_key, self.target_lang
        ).split(' ')
        settings = Settings()
        with self.assertRaises(ConfigurationError):
            settings.source_lang
