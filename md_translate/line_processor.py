import re

from md_translate.settings import Settings
from md_translate import const


class LineProcessor:
    code_mark: str = '```'
    TRANSLATION_CHECK_REGEXP_BY_LANG = {
        const.LANG_RU: r'^[а-яА-Я]+.*',
        const.LANG_EN: r'^[a-zA-Z]+.*',
    }
    DEFAULT_TRANSLATION_CHECK_REGEXP_BY_LANG = r'^\d+.*'

    def __init__(self, settings: Settings, line: str) -> None:
        self.settings = settings
        self._line: str = line
        self.pattern = self.TRANSLATION_CHECK_REGEXP_BY_LANG.get(
            self.settings.source_lang, self.DEFAULT_TRANSLATION_CHECK_REGEXP_BY_LANG
        )

    def is_code_block_border(self) -> bool:
        if self._line == self.code_mark:
            return True
        return self._line.startswith(self.code_mark) and not self._line.endswith(
            self.code_mark
        )

    def line_can_be_translated(self) -> bool:
        return not self.__is_single_code_line() and self.__is_untranslated_paragraph()

    def __is_untranslated_paragraph(self) -> bool:
        return re.match(self.pattern, self._line) is not None

    def __is_single_code_line(self) -> bool:
        return (
            self._line.startswith(self.code_mark)
            and self._line.endswith(self.code_mark)
            and len(self._line) > 3
        )
