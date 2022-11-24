import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

import pytest

from md_translate.file_translator import FileTranslator

fixture = Path('tests/test_data/fixture.md')
fixture_translated = Path('tests/test_data/fixture_translated.md')
fixture_translated_replaced = Path('tests/test_data/fixture_translated.md')
file_to_test_on = Path('tests/test_data/file_to_test_on.md')


@pytest.fixture()
def temp_test_file():
    file_to_test_on.write_text(fixture.read_text())
    yield
    file_to_test_on.unlink()


class TestFileTranslator:
    @mock.patch('md_translate.line_processor.get_translator_by_service_name')
    @pytest.mark.parametrize('do_replace, result_file_path', [
        [False, 'tests/test_data/fixture_translated.md'],
        [True, 'tests/test_data/fixture_translated_replace.md'],
    ])
    def test_file_translator(self, get_translator_mock, temp_test_file, do_replace, result_file_path):
        class SettingsMock:
            service_name = 'Yandex'
            source_lang = 'en'
            target_lang = 'ru'
            api_key = 'TEST_API_KEY'
            replace = do_replace

        translator_mock = Mock()
        translator_mock.return_value = 'Переведенная строка'
        get_translator_mock.return_value = translator_mock
        with FileTranslator(SettingsMock(), file_to_test_on) as file_translator:
            assert isinstance(file_translator, FileTranslator)
            file_translator.translate()
        get_translator_mock.assert_called_with(SettingsMock.service_name)
        translator_mock.assert_called_with('Some string for translation\n', from_language='en', to_language='ru')

        assert file_to_test_on.read_text() == Path(result_file_path).read_text()
