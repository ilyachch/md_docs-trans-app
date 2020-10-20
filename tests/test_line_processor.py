from unittest import mock
import pytest

from md_translate import const
from md_translate.line_processor import Line


@pytest.fixture()
def en_ru_settings():
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = const.TRANSLATION_SERVICE_YANDEX

    return MockedSettings()


@pytest.fixture()
def ru_en_settings():
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'ru'
        target_lang = 'en'
        service = const.TRANSLATION_SERVICE_YANDEX

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
        assert Line(en_ru_settings, line).is_code_block_border == valid


class TestLineProcessorEnRu:
    @pytest.mark.parametrize('line, valid, line_lang', [
        ['Test string', True, ],
        ['Тестовая строка', False, ],
        ['> Quote', True, ],
        ['* List Item', True, ],
        ['```', False, ],
        ['```python', False, ],
        ['```bash', False, ],
        ['```Some_String```', False, ],
    ])
    def test_line_can_be_translated(self, line, valid, line_lang, en_ru_settings):
        with mock.patch('md_translate.line_processor.detect') as detect_mock:
            detect_mock.return_value = 'en'
            assert Line(en_ru_settings, line).line_can_be_translated == valid


class TestLineProcessorRuEn:
    @pytest.mark.parametrize('line, valid, line_lang', [
        ['Лорем ипсум', True, ],
        ['Lorem Ipsum', False, ],
        ['> Цитата', True, ],
        ['* Элемент списка', True, ],
        ['```', False, ],
        ['```python', False, ],
        ['```bash', False, ],
        ['```Some_String```', False, ],
    ])
    def test_line_can_be_translated(self, line, valid, line_lang, ru_en_settings):
        with mock.patch('md_translate.line_processor.detect') as detect_mock:
            detect_mock.return_value = 'ru'
            assert Line(ru_en_settings, line).line_can_be_translated == valid
