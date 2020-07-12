import unittest
from unittest.mock import patch

from md_translate.line_processor import LineProcessor
from md_translate import const

CODE_BLOCK_STR = '```'
PYTHON_CODE_BLOCK_STR = '```python'
BASH_CODE_BLOCK_STR = '```bash'
SINGLE_LINE_CODE_BLOCK_STR = '```Some_String```'
NOT_CODE_BLOCK_STR = 'Some Data'

PARAGRAPH_STR_EN = 'Lorem Ipsum'
TRANSLATED_PARAGRAPH_STR_RU = 'Лорем ипсум'
PARAGRAPH_STR_RU = 'Лорем ипсум'
TRANSLATED_PARAGRAPH_STR_EN = 'Lorem Ipsum'
QUOTE_BLOCK_STR = '> Quote'
LIST_ITEM_STR = '* List Item'


class MockedSettingsEnRu:
    api_key = 'TEST_API_KEY'
    source_lang = const.LANG_EN
    target_lang = const.LANG_RU
    service = const.TRANSLATION_SERVICE_YANDEX


class MockedSettingsRuEn:
    api_key = 'TEST_API_KEY'
    source_lang = const.LANG_RU
    target_lang = const.LANG_EN
    service = const.TRANSLATION_SERVICE_YANDEX


class TestLineProcessorWithCode(unittest.TestCase):
    @patch('md_translate.line_processor.get_settings')
    def test_common_blocks(self, get_settings_mock):
        get_settings_mock.return_value = MockedSettingsEnRu()
        self.assertTrue(LineProcessor(BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(NOT_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(LIST_ITEM_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(CODE_BLOCK_STR).line_can_be_translated())

    @patch('md_translate.line_processor.get_settings')
    def test_code_block_border_en_ru(self, get_settings_mock):
        get_settings_mock.return_value = MockedSettingsEnRu()
        self.assertTrue(LineProcessor(CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(PYTHON_CODE_BLOCK_STR).is_code_block_border())

    @patch('md_translate.line_processor.get_settings')
    def test_line_can_be_translated_en_ru(self, get_settings_mock):
        get_settings_mock.return_value = MockedSettingsEnRu()
        self.assertTrue(LineProcessor(PARAGRAPH_STR_EN).line_can_be_translated())
        self.assertFalse(LineProcessor(TRANSLATED_PARAGRAPH_STR_RU).line_can_be_translated())

    @patch('md_translate.line_processor.get_settings')
    def test_code_block_border_ru_en(self, get_settings_mock):
        get_settings_mock.return_value = MockedSettingsRuEn()
        self.assertTrue(LineProcessor(CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(PYTHON_CODE_BLOCK_STR).is_code_block_border())

    @patch('md_translate.line_processor.get_settings')
    def test_line_can_be_translated_ru_en(self, get_settings_mock):
        get_settings_mock.return_value = MockedSettingsRuEn()
        self.assertTrue(LineProcessor(PARAGRAPH_STR_RU).line_can_be_translated())
        self.assertFalse(LineProcessor(TRANSLATED_PARAGRAPH_STR_EN).line_can_be_translated())
