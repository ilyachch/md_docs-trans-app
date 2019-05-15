import unittest
from pathlib import Path
from unittest import mock

from md_translate.file_translator import FileTranslator


class TestFileTranslator(unittest.TestCase):
    fixture = Path('tests/test_data/fixture.md')
    fixture_translated = Path('tests/test_data/fixture_translated.md')
    file_to_test_on = Path('tests/test_data/file_to_test_on.md')

    def setUp(self):
        class SettingsMock:
            service = 'Yandex'
            source_lang = 'en'
            target_lang = 'ru'

        self.settings_mock = SettingsMock()

        with self.fixture.open() as fixture:
            with self.file_to_test_on.open('w') as target:
                target.write(fixture.read())

    def tearDown(self) -> None:
        self.file_to_test_on.unlink()

    @mock.patch('md_translate.translator.YandexTranslator')
    def test_file_translator(self, translator_mock):
        translator_mock().request_translation.return_value = 'Переведенная строка'
        with FileTranslator(self.settings_mock, self.file_to_test_on) as file_translator:
            self.assertIsInstance(file_translator, FileTranslator)
            file_translator.translate()
        translator_mock().request_translation.assert_called_with('Some string for translation\n')

        with self.file_to_test_on.open() as fixture:
            with self.fixture_translated.open() as fixture_translated:
                self.assertEqual(fixture.read(), fixture_translated.read())
