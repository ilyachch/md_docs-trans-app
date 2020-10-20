from typing import TYPE_CHECKING

from langdetect import detect  # type: ignore
from langdetect.lang_detect_exception import LangDetectException  # type: ignore

if TYPE_CHECKING:
    from md_translate.settings import Settings


class Line:
    code_mark: str = '```'
    list_item_mark = '* '
    quote_item_mark = '> '

    def __init__(self, settings: 'Settings', line: str) -> None:
        self.settings = settings
        self._line: str = line

    def __str__(self) -> str:  # pragma: no cover
        return self._line

    def __repr__(self) -> str:  # pragma: no cover
        return f'{self.__class__.__name__}: {self._line}'

    @property
    def is_code_block_border(self) -> bool:
        if self._line == self.code_mark:
            return True
        return self._line.startswith(self.code_mark) and not self._line.endswith(
            self.code_mark
        )

    @property
    def line_can_be_translated(self) -> bool:
        return (
            # not self.__is_quote_string() and
            # not self.__is_list_item_string() and
            not self.is_code_block_border and
            not self.__is_single_code_line() and
            self.__is_untranslated_paragraph()
        )

    def __is_untranslated_paragraph(self) -> bool:
        try:
            return detect(self._line) == self.settings.source_lang
        except LangDetectException:
            return False

    def __is_single_code_line(self) -> bool:
        return (
            self._line.startswith(self.code_mark)
            and self._line.endswith(self.code_mark)
            and len(self._line) > 3
        )

    # def __is_list_item_string(self) -> bool:
    #     return self._line.startswith(self.list_item_mark)
    #
    # def __is_quote_string(self) -> bool:
    #     return self._line.startswith(self.quote_item_mark)
