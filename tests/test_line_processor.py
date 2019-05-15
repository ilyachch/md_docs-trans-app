import unittest

from md_translate.line_processor import LineProcessor


class TestLineProcessorWithCodeEnRu(unittest.TestCase):
    CODE_BLOCK_STR = '```'
    PYTHON_CODE_BLOCK_STR = '```python'
    BASH_CODE_BLOCK_STR = '```bash'
    SINGLE_LINE_CODE_BLOCK_STR = '```Some_String```'
    NOT_CODE_BLOCK_STR = 'Some Data'

    PARAGRAPH_STR = 'Lorem Ipsum'
    TRANSLATED_PARAGRAPH_STR = 'Лорем ипсум'
    QUOTE_BLOCK_STR = '> Quote'
    LIST_ITEM_STR = '* List Item'

    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = 'Yandex'

    def setUp(self) -> None:
        self.settings = self.MockedSettings()

    def test_code_block_border(self):
        self.assertTrue(LineProcessor(self.settings, self.CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.settings, self.PYTHON_CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.settings, self.BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.settings, self.NOT_CODE_BLOCK_STR).is_code_block_border())

    def test_line_can_be_translated(self):
        self.assertTrue(LineProcessor(self.settings, self.PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.TRANSLATED_PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.LIST_ITEM_STR).line_can_be_translated())


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
        service = 'Yandex'

    def setUp(self) -> None:
        self.settings = self.MockedSettings()

    def test_code_block_border(self):
        self.assertTrue(LineProcessor(self.settings, self.CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.settings, self.PYTHON_CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.settings, self.BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.settings, self.NOT_CODE_BLOCK_STR).is_code_block_border())

    def test_line_can_be_translated(self):
        self.assertTrue(LineProcessor(self.settings, self.PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.TRANSLATED_PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.settings, self.LIST_ITEM_STR).line_can_be_translated())


class TestLineProcessorGetRegex(unittest.TestCase):
    def test_ru_regex(self):
        self.assertEqual(LineProcessor.get_regexp('ru'), r'^[а-яА-Я]+.*')

    def test_en_regex(self):
        self.assertEqual(LineProcessor.get_regexp('en'), r'^[a-zA-Z]+.*')

    def test_common_regex(self):
        self.assertEqual(LineProcessor.get_regexp(), r'^\d+.*')
