import pathlib
import re
from typing import Type, IO, Any, TYPE_CHECKING

from md_translate.line_processor import LineProcessor
from md_translate.utils import get_translator_class_by_service_name, get_settings

if TYPE_CHECKING:
    from md_translate.translator import AbstractTranslator


class FileTranslator:
    default_open_mode: str = 'r+'

    code_mark: str = '```'
    paragraph_regexp = re.compile(r'^[a-zA-Z]+.*')

    def __init__(self, file_path: pathlib.Path):
        self.settings = get_settings()
        translator_class: Type[
            'AbstractTranslator'
        ] = get_translator_class_by_service_name(self.settings.service_name)
        self.__translator: 'AbstractTranslator' = translator_class()
        self.__file_path: pathlib.Path = file_path
        self.file_contents_with_translation: list = []
        self.code_block: bool = False

    def __enter__(self) -> 'FileTranslator':
        self.__translating_file: IO = self.__file_path.open(self.default_open_mode)
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.__translating_file.close()

    def translate(self) -> None:
        lines = self.__translating_file.readlines()
        for counter, line in enumerate(lines):
            self.file_contents_with_translation.append(line)
            line_processor = LineProcessor(line)
            self.code_block = (
                not self.code_block
                if line_processor.is_code_block_border()
                else self.code_block
            )
            if line_processor.line_can_be_translated() and not self.code_block:
                translated = self.__translator.request_translation(line)
                self.file_contents_with_translation.append('\n')
                if line.endswith('\n') and not translated.endswith('\n'):
                    self.file_contents_with_translation.append(
                        ''.join([translated, '\n'])
                    )
                else:
                    self.file_contents_with_translation.append(translated)
        self.__write_translated_data_to_file()

    def __write_translated_data_to_file(self) -> None:
        self.__translating_file.seek(0)
        self.__translating_file.writelines(self.file_contents_with_translation)
