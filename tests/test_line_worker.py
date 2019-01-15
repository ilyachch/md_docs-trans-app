import unittest

from md_translate.line_processor import LineProcessor


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

    def test_code_block_border(self):
        self.assertTrue(LineProcessor(self.CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.PYTHON_CODE_BLOCK_STR).is_code_block_border())
        self.assertTrue(LineProcessor(self.BASH_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.SINGLE_LINE_CODE_BLOCK_STR).is_code_block_border())
        self.assertFalse(LineProcessor(self.NOT_CODE_BLOCK_STR).is_code_block_border())

    def test_line_can_be_translated(self):
        self.assertTrue(LineProcessor(self.PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.PYTHON_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.BASH_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.SINGLE_LINE_CODE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.TRANSLATED_PARAGRAPH_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.QUOTE_BLOCK_STR).line_can_be_translated())
        self.assertFalse(LineProcessor(self.LIST_ITEM_STR).line_can_be_translated())
