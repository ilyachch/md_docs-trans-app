import unittest
from unittest import mock

from md_translate.line_processor import LineProcessor


class MockedSettings:
    api_key = 'TEST_API_KEY'
    source_lang = 'en'
    target_lang = 'ru'
    service = 'Yandex'


class TestLineProcessorWithCode(unittest.TestCase):
    CODE_BLOCK_STR = '```'
    PYTHON_CODE_BLOCK_STR = '```python'
    BASH_CODE_BLOCK_STR = '```bash'
    SINGLE_LINE_CODE_BLOCK_STR = '```Some_String```'
    NOT_CODE_BLOCK_STR = 'Some Data'

    PARAGRAPH_STR = 'Lorem Ipsum'
    TRANSLATED_PARAGRAPH_STR = 'Лорем ипсум'
    QUOTE_BLOCK_STR = '> Quote'
    LIST_ITEM_STR = '* List Item'

    @mock.patch('md_translate.line_processor.settings', new_callable=MockedSettings)
    def test_code_block_border(self, mocked_settings):
        self.assertTrue(LineProcessor(self.CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.PYTHON_CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.NOT_CODE_BLOCK_STR).is_code_block_border())

    @mock.patch('md_translate.line_processor.settings', new_callable=MockedSettings)
    def test_line_can_be_translated(self, mocked_settings):
        self.assertTrue(LineProcessor(self.PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.TRANSLATED_PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.LIST_ITEM_STR).line_can_be_translated())
