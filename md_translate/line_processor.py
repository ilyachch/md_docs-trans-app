import re


class LineProcessor:
    code_mark = '```'
    paragraph_regexp = re.compile(r'^[a-zA-Z]+.*')

    def __init__(self, line):
        """

        :param line: str
        """
        self._line = line

    def is_code_block_border(self):
        if self._line == self.code_mark:
            return True
        return self._line.startswith(self.code_mark) and not self._line.endswith(self.code_mark)

    def line_can_be_translated(self):
        return not self.__is_single_code_line() and self.__is_untranslated_paragraph()

    def __is_untranslated_paragraph(self):
        return self.paragraph_regexp.match(self._line)

    def __is_single_code_line(self):
        return self._line.startswith(self.code_mark) and self._line.endswith(self.code_mark) and len(self._line) > 3
