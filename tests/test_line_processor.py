from unittest import mock

import pytest
from langdetect.lang_detect_exception import LangDetectException

from md_translate import const
from md_translate.line_processor import Line

detect_path = 'md_translate.line_processor.detect'

@pytest.fixture()
def en_ru_settings():
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service_name = const.TRANSLATION_SERVICE_YANDEX

    return MockedSettings()


@pytest.fixture()
def ru_en_settings():
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'ru'
        target_lang = 'en'
        service_name = const.TRANSLATION_SERVICE_YANDEX
        replace = False

    return MockedSettings()


class TestLineProcessor:
    @pytest.mark.parametrize('line, valid', [
        ['```', True],
        ['```python', True],
        ['```bash', True],
        ['```Some_String```', False],
        ['Some Data', False],
    ])
    def test_is_code_block_border(self, line, valid, en_ru_settings):
        line = Line(en_ru_settings, line)
        assert line.is_code_block_border() == valid

    @pytest.mark.parametrize('line, valid, line_lang', [
        ['Test string', True, 'en'],
        ['Тестовая строка', False, 'ru'],
        ['> Quote', True, 'en'],
        ['* List Item', True, 'en'],
        ['```', False, 'en'],
        ['```python', False, 'en'],
        ['```bash', False, 'en'],
        ['```Some_String```', False, 'en'],
    ])
    def test_line_can_be_translated_en_ru(
            self, line, valid, line_lang, en_ru_settings
    ):
        with mock.patch(detect_path) as detect_mock:
            detect_mock.return_value = line_lang
            assert Line(en_ru_settings, line).can_be_translated() == valid

    @pytest.mark.parametrize('line, valid, line_lang', [
        ['Лорем ипсум', True, 'ru'],
        ['Lorem Ipsum', False, 'en'],
        ['> Цитата', True, 'ru'],
        ['* Элемент списка', True, 'ru'],
        ['```', False, 'ru'],
        ['```python', False, 'ru'],
        ['```bash', False, 'ru'],
        ['```Some_String```', False, 'ru'],
    ])
    def test_line_can_be_translated_ru_en(
            self, line, valid, line_lang, ru_en_settings
    ):
        with mock.patch(detect_path) as detect_mock:
            detect_mock.return_value = line_lang
            assert Line(ru_en_settings, line).can_be_translated() == valid


@pytest.mark.parametrize('line', [
    'Лорем ипсум',
    'Lorem Ipsum',
    '> Цитата',
    '* Элемент списка',
    'Test string',
    'Тестовая строка',
    '> Quote',
    '* List Item',
    '```',
    '```python',
    '```bash',
    '```Some_String```',
])
class TestLineProcessorUniversal:
    def test_line_can_be_translated_error(self, line, en_ru_settings):
        with mock.patch(detect_path) as detect_mock:
            detect_mock.side_effect = LangDetectException(1, 'Boom!')
            assert not Line(en_ru_settings, line).can_be_translated()

    def test_type_methods(self, line, en_ru_settings):
        line_inst = Line(en_ru_settings, line)
        assert str(line_inst) == line
        assert repr(line_inst) == f'Line: "{line}"'

    def test_properties(self, line, en_ru_settings):
        with mock.patch(detect_path) as detect_mock:
            detect_mock.return_value = 'ru'
            line_ints = Line(en_ru_settings, line)
            assert line_ints.original == line
            assert line_ints.fixed == line
            assert line_ints.translated == line
