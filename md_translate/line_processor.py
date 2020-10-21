from typing import TYPE_CHECKING

from langdetect import detect  # type: ignore
from langdetect.lang_detect_exception import LangDetectException  # type: ignore

from md_translate.utils import get_translator_by_service_name

if TYPE_CHECKING:
    from md_translate.settings import Settings


class Line:
    code_mark: str = '```'
    list_item_mark = '* '
    quote_item_mark = '> '

    new_line_symb = '\n'

    def __init__(self, settings: 'Settings', line: str) -> None:
        self.settings = settings
        self._translator = get_translator_by_service_name(self.settings.service_name)
        self._line: str = line
        self._translated_line = ''

    def __str__(self) -> str:
        return self._line

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: "{self._line}"'

    @property
    def original(self) -> str:
        return self._line

    @property
    def translated(self) -> str:
        if not self._translated_line and self.can_be_translated():
            self._translate()
        return self._translated_line or self.original

    @property
    def fixed(self) -> str:
        if self._line.endswith('\n') and not self.translated.endswith('\n'):
            return ''.join([self.translated, '\n'])
        return self.translated

    def is_code_block_border(self) -> bool:
        if self._line == self.code_mark:
            return True
        return self._line.startswith(self.code_mark) and not self._line.endswith(
            self.code_mark
        )

    def can_be_translated(self) -> bool:
        return (
            not self._is_empty_line()
            and not self.is_code_block_border()
            and not self._is_single_code_line()
            and self._is_untranslated_paragraph()
        )

    def _translate(self) -> None:
        self._translated_line = self._translator(
            self._line,
            from_language=self.settings.source_lang,
            to_language=self.settings.target_lang,
        )

    def _is_untranslated_paragraph(self) -> bool:
        try:
            return detect(self._line) == self.settings.source_lang
        except LangDetectException:
            return False

    def _is_single_code_line(self) -> bool:
        return (
            self._line.startswith(self.code_mark)
            and self._line.endswith(self.code_mark)
            and len(self._line) > 3
        )

    def _is_empty_line(self) -> bool:
        if self._line == self.new_line_symb:
            return True
        return not bool(self._line)
