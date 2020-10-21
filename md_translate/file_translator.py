from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, List

from md_translate.line_processor import Line
from md_translate.logs import logger

if TYPE_CHECKING:
    from md_translate.settings import Settings


class FileTranslator:
    default_open_mode: str = 'r+'

    def __init__(self, settings: 'Settings', file_path: Path) -> None:
        self.settings = settings
        self.file_path: Path = file_path
        self.file_contents_with_translation: list = []
        self.code_block: bool = False

    def __enter__(self) -> 'FileTranslator':
        self.__translating_file: IO = self.file_path.open(self.default_open_mode)
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.__translating_file.close()

    def translate(self) -> None:
        lines = self._get_lines()
        for counter, _line in enumerate(lines):
            line = Line(self.settings, _line)
            self.file_contents_with_translation.append(line.original)
            self.code_block = (
                not self.code_block if line.is_code_block_border() else self.code_block
            )
            if line.can_be_translated() and not self.code_block:
                self.file_contents_with_translation.append('\n')
                self.file_contents_with_translation.append(line.fixed)
                logger.info(f'Processed {counter+1} lines')
        self._write_translated_data_to_file()

    def _get_lines(self) -> List[str]:
        lines = self.__translating_file.readlines()
        logger.info(f'Got {len(lines)} lines to process')
        return lines

    def _write_translated_data_to_file(self) -> None:
        self.__translating_file.seek(0)
        self.__translating_file.writelines(self.file_contents_with_translation)
