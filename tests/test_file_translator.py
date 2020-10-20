import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

from md_translate.file_translator import FileTranslator


class TestFileTranslator(unittest.TestCase):
    fixture = Path('tests/test_data/fixture.md')
    fixture_translated = Path('tests/test_data/fixture_translated.md')
    file_to_test_on = Path('tests/test_data/file_to_test_on.md')

    def setUp(self):
        with self.fixture.open() as fixture:
            with self.file_to_test_on.open('w') as target:
                target.write(fixture.read())

    def tearDown(self) -> None:
        self.file_to_test_on.unlink()

    @mock.patch('md_translate.file_translator.get_translator_by_service_name')
    def test_file_translator(self, get_translator_mock):
        class SettingsMock:
            service_name = 'Yandex'
            source_lang = 'en'
            target_lang = 'ru'
            api_key = 'TEST_API_KEY'

        translator_mock = Mock()
        translator_mock.return_value = 'Переведенная строка'
        get_translator_mock.return_value = translator_mock
        with FileTranslator(SettingsMock(), self.file_to_test_on) as file_translator:
            self.assertIsInstance(file_translator, FileTranslator)
            file_translator.translate()
        translator_mock.assert_called_with('Some string for translation\n', from_language='en', to_language='ru')

        with self.file_to_test_on.open() as fixture:
            with self.fixture_translated.open() as fixture_translated:
                self.assertEqual(fixture.read(), fixture_translated.read())
