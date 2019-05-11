import pathlib
import re
from typing import Type, Union, IO

from md_translate.arguments_processor import settings
from md_translate.line_processor import LineProcessor
from md_translate.translator import get_translator_by_name, Translator


class FileTranslator:
    default_open_mode: str = 'r+'

    code_mark: str = '```'
    paragraph_regexp = re.compile(r'^[a-zA-Z]+.*')

    def __init__(self, file_path: pathlib.Path):
        translator_class: Type[Translator] = get_translator_by_name(settings.service)
        self.__translator = translator_class()
        self.__file_path: pathlib.Path = file_path
        self.line_processor: Union[LineProcessor, None] = None
        self.file_contents_with_translation: list = []
        self.code_block: bool = False

    def __enter__(self):
        self.__translating_file: IO = self.__file_path.open(self.default_open_mode)
        return self

    def __exit__(self, *args, **kwargs):
        self.__translating_file.close()

    def translate(self):
        lines = self.__translating_file.readlines()
        for counter, line in enumerate(lines):
            self.file_contents_with_translation.append(line)
            self.line_processor = LineProcessor(line)
            self.code_block = not self.code_block if self.line_processor.is_code_block_border() else self.code_block
            if self.line_processor.line_can_be_translated() and not self.code_block:
                translated = self.__translator.request_translation(line)
                self.file_contents_with_translation.append('\n')
                self.file_contents_with_translation.append(translated)

                print('Processed: {percent}% ({counter} of {lines})'.format(percent=(counter / len(lines) * 100),
                                                                            counter=counter, lines=len(lines)))

        self.__write_translated_data_to_file()

    def __write_translated_data_to_file(self):
        self.__translating_file.seek(0)
        self.__translating_file.writelines(self.file_contents_with_translation)
