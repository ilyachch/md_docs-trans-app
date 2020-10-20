from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, List

from md_translate.line_processor import Line
from md_translate.logs import logger
from md_translate.utils import get_translator_by_service_name

if TYPE_CHECKING:
    from md_translate.settings import Settings


class FileTranslator:
    default_open_mode: str = 'r+'

    def __init__(self, settings: 'Settings', file_path: Path) -> None:
        self.settings = settings
        self.__translator = get_translator_by_service_name(settings.service_name)
        self.__file_path: Path = file_path
        self.file_contents_with_translation: list = []
        self.code_block: bool = False

    def __enter__(self) -> 'FileTranslator':
        self.__translating_file: IO = self.__file_path.open(self.default_open_mode)
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.__translating_file.close()

    def translate(self) -> None:
        lines = self.get_lines()
        for counter, line in enumerate(lines):
            self.file_contents_with_translation.append(line)
            line_processor = Line(self.settings, line)
            self.code_block = (
                not self.code_block
                if line_processor.is_code_block_border
                else self.code_block
            )
            if line_processor.line_can_be_translated and not self.code_block:
                translated = self.get_translated_line(line)
                self.file_contents_with_translation.append('\n')
                if line.endswith('\n') and not translated.endswith('\n'):
                    self.file_contents_with_translation.append(
                        ''.join([translated, '\n'])
                    )
                else:
                    self.file_contents_with_translation.append(
                        translated
                    )  # pragma: no cover

                logger.info(f'Processed {counter+1} lines')
        self.__write_translated_data_to_file()

    def get_translated_line(self, line: str) -> str:
        return self.__translator(
            line,
            from_language=self.settings.source_lang,
            to_language=self.settings.target_lang,
        )

    def get_lines(self) -> List[str]:
        lines = self.__translating_file.readlines()
        logger.info(f'Got {len(lines)} lines to process')
        return lines

    def __write_translated_data_to_file(self) -> None:
        self.__translating_file.seek(0)
        self.__translating_file.writelines(self.file_contents_with_translation)
