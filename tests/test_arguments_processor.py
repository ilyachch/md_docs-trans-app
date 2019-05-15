import configparser
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, PropertyMock

from md_translate.arguments_processor import ArgumentsProcessor
from md_translate.exceptions import NoConfigFileError, ConfigurationError


class TestArgumentsProcessorWithoutSettings(TestCase):
    def setUp(self) -> None:
        self.current_path = Path().cwd()
        self.test_path = Path('tests/test_data/md_files_folder')
        self.test_settings_file = Path('tests/test_data/settings.ini')
        self.api_key = 'API_KEY'
        self.service = 'Yandex'
        self.source_lang = 'en'
        self.target_lang = 'ru'

    def test_typical_launch(self):
        processor = ArgumentsProcessor('-K {} -s {} -S {} -T {}'.format(
            self.api_key, self.service, self.source_lang, self.target_lang
        ).split(' '))
        self.assertEqual(processor.path, self.current_path)
        self.assertEqual(processor.api_key, self.api_key)
        self.assertEqual(processor.service, self.service)
        self.assertEqual(processor.source_lang, self.source_lang)
        self.assertEqual(processor.target_lang, self.target_lang)

    def test_launch_with_path(self):
        processor = ArgumentsProcessor('{} -K {} -s {} -S {} -T {}'.format(
            self.test_path, self.api_key, self.service, self.source_lang, self.target_lang
        ).split(' '))
        self.assertEqual(processor.path, self.test_path)
        self.assertEqual(processor.api_key, self.api_key)
        self.assertEqual(processor.service, self.service)
        self.assertEqual(processor.source_lang, self.source_lang)
        self.assertEqual(processor.target_lang, self.target_lang)


class TestArgumentsProcessorWithSettings(TestCase):
    def setUp(self) -> None:
        self.test_path = Path('test_data/md_files_folder')
        self.api_key = 'FILE_API_KEY'
        self.api_key_override = 'OVERRIDE_API_KEY'
        self.service = 'Yandex'
        self.service_override = 'Google'
        self.source_lang = 'ru'
        self.source_lang_override = 'en'
        self.target_lang = 'en'
        self.target_lang_override = 'ru'
        self.test_settings_file = Path('tests/test_data/settings.ini')
        self.__create_test_settings_file()

    def __create_test_settings_file(self):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'api_key ': self.api_key,
            'service ': self.service,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
        }
        with self.test_settings_file.open('w') as settings_file:
            config.write(settings_file)

    def tearDown(self) -> None:
        self.test_settings_file.unlink()

    def test_launch_with_settings_file(self):
        args = '{} -c {}'.format(self.test_path, str(self.test_settings_file)).split(' ')
        processor = ArgumentsProcessor(args)
        self.assertEqual(processor.path, self.test_path)
        self.assertEqual(processor.api_key, self.api_key)
        self.assertEqual(processor.service, self.service)
        self.assertEqual(processor.source_lang, self.source_lang)
        self.assertEqual(processor.target_lang, self.target_lang)

    def test_params_overide(self):
        args = '-c {} -K {} -s {} -S {} -T {}'.format(
            str(self.test_settings_file), self.api_key_override, self.service_override,
            self.source_lang_override, self.target_lang_override
        ).split(' ')
        processor = ArgumentsProcessor(args)
        self.assertEqual(processor.api_key, self.api_key_override)
        self.assertEqual(processor.service, self.service_override)
        self.assertEqual(processor.source_lang, self.source_lang_override)
        self.assertEqual(processor.target_lang, self.target_lang_override)

    def test_default_config_usage_without_params(self):
        with patch('md_translate.arguments_processor.ArgumentsProcessor.CONFIG_FILE_DEFAULT_PATH',
                   new_callable=PropertyMock, return_value=self.test_settings_file):
            processor = ArgumentsProcessor([])
            self.assertEqual(processor.api_key, self.api_key)
            self.assertEqual(processor.service, self.service)
            self.assertEqual(processor.source_lang, self.source_lang)
            self.assertEqual(processor.target_lang, self.target_lang)


class TestArgumentsProcessorWithApiKeyFile(TestCase):
    def setUp(self) -> None:
        self.test_path = Path('tests/test_data/md_files_folder')
        self.api_key = 'FILE_API_KEY'
        self.service = 'Yandex'
        self.source_lang = 'ru'
        self.target_lang = 'en'
        self.test_api_key_file = Path('tests/test_data/api_key_file')
        self.__create_api_key_file()

    def __create_api_key_file(self):
        with self.test_api_key_file.open('w') as api_key_file:
            api_key_file.write(self.api_key)

    def tearDown(self):
        self.test_api_key_file.unlink()

    def test_launch_with_api_key_file(self):
        args = '-k {} -s {} -S {} -T {}'.format(
            str(self.test_api_key_file), self.service, self.source_lang, self.target_lang
        ).split(' ')
        processor = ArgumentsProcessor(args)
        self.assertEqual(processor.api_key, self.api_key)

    def test_launch_with_default_api_key_file(self):
        args = '-s {} -S {} -T {}'.format(self.service, self.source_lang, self.target_lang).split(' ')
        with patch('md_translate.arguments_processor.ArgumentsProcessor.TRANSLATOR_API_KEY_FILE_DEFAULT_PATH',
                   new_callable=PropertyMock, return_value=self.test_api_key_file):
            processor = ArgumentsProcessor(args)
            self.assertEqual(processor.api_key, self.api_key)


class TestArgumentsProcessorErrors(TestCase):
    def setUp(self) -> None:
        self.test_path = Path('tests/test_data/md_files_folder')
        self.api_key = 'FILE_API_KEY'
        self.service = 'Yandex'
        self.source_lang = 'ru'
        self.target_lang = 'en'
        self.config_file = Path('tests/test_data/config_file')
        self.__create_config_file()

    def tearDown(self) -> None:
        self.config_file.unlink()

    def __create_config_file(self):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'service ': self.service,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
        }
        with self.config_file.open('w') as settings_file:
            config.write(settings_file)

    def test_validate_setup_no_config_file(self):
        processor = ArgumentsProcessor()
        with self.assertRaises(NoConfigFileError):
            processor.validate_arguments()

    def test_validate_setup_configuration_error(self):
        with patch('md_translate.arguments_processor.ArgumentsProcessor.CONFIG_FILE_DEFAULT_PATH',
                   new_callable=PropertyMock, return_value=self.config_file):
            args = '-s {} -S {} -T {}'.format(self.service, self.source_lang, self.target_lang).split(' ')
            with self.assertRaises(ConfigurationError):
                ArgumentsProcessor(args).validate_arguments()

    # TODO: fix this test
    # def test_launch_with_conflict_params(self):
    #     args = '-k {} -K {} -s {} -S {} -T {}'.format(
    #         self.api_key, self.test_api_key_file, self.service, self.source_lang, self.target_lang
    #     ).split()
    #     with self.assertRaises(ArgumentError):
    #         ArgumentsProcessor(args)
