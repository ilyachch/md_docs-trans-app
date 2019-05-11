import re
from md_translate.arguments_processor import settings


class LineProcessor:
    code_mark: str = '```'

    def __init__(self, line: str):
        self._line: str = line
        self.pattern = self.get_regexp(settings.source_lang)

    def is_code_block_border(self):
        if self._line == self.code_mark:
            return True
        return self._line.startswith(self.code_mark) and not self._line.endswith(self.code_mark)

    def line_can_be_translated(self):
        return not self.__is_single_code_line() and self.__is_untranslated_paragraph()

    def __is_untranslated_paragraph(self):
        return re.match(self.pattern, self._line) is not None

    def __is_single_code_line(self):
        return self._line.startswith(self.code_mark) and self._line.endswith(self.code_mark) and len(self._line) > 3

    @staticmethod
    def get_regexp(source_lang):
        if source_lang == 'ru':
            return r'^[а-яА-Я]+.*'
        elif source_lang == 'en':
            return r'^[a-zA-Z]+.*'
        else:
            return r'^\d+.*'
