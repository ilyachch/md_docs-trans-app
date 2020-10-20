import unittest

from md_translate.line_processor import Line
from md_translate import const

class TestLineProcessorWithCodeEnRu(unittest.TestCase):
    CODE_BLOCK_STR = '```'
    PYTHON_CODE_BLOCK_STR = '```python'
    BASH_CODE_BLOCK_STR = '```bash'
    SINGLE_LINE_CODE_BLOCK_STR = '```Some_String```'
    NOT_CODE_BLOCK_STR = 'Some Data'

    PARAGRAPH_STR = 'Test string'
    TRANSLATED_PARAGRAPH_STR = 'Тестовая строка'
    QUOTE_BLOCK_STR = '> Quote'
    LIST_ITEM_STR = '* List Item'

    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = const.TRANSLATION_SERVICE_YANDEX

    def setUp(self) -> None:
        self.settings = self.MockedSettings()

    def test_code_block_border(self):
        self.assertTrue(Line(self.settings, self.CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(Line(self.settings, self.PYTHON_CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(Line(self.settings, self.BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(Line(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(Line(self.settings, self.NOT_CODE_BLOCK_STR).is_code_block_border())

    def test_line_can_be_translated(self):
        self.assertTrue(Line(self.settings, self.PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.TRANSLATED_PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.LIST_ITEM_STR).line_can_be_translated())


class TestLineProcessorWithCodeRuEn(unittest.TestCase):
    CODE_BLOCK_STR = '```'
    PYTHON_CODE_BLOCK_STR = '```python'
    BASH_CODE_BLOCK_STR = '```bash'
    SINGLE_LINE_CODE_BLOCK_STR = '```Some_String```'
    NOT_CODE_BLOCK_STR = 'Some Data'

    PARAGRAPH_STR = 'Лорем ипсум'
    TRANSLATED_PARAGRAPH_STR = 'Lorem Ipsum'
    QUOTE_BLOCK_STR = '> Quote'
    LIST_ITEM_STR = '* List Item'

    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'ru'
        target_lang = 'en'
        service = const.TRANSLATION_SERVICE_YANDEX

    def setUp(self) -> None:
        self.settings = self.MockedSettings()

    def test_code_block_border(self):
        self.assertTrue(Line(self.settings, self.CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(Line(self.settings, self.PYTHON_CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(Line(self.settings, self.BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(Line(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(Line(self.settings, self.NOT_CODE_BLOCK_STR).is_code_block_border())

    def test_line_can_be_translated(self):
        self.assertTrue(Line(self.settings, self.PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.TRANSLATED_PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(Line(self.settings, self.LIST_ITEM_STR).line_can_be_translated())
