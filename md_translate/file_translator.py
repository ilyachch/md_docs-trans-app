import re

from md_translate.line_processor import LineProcessor
from md_translate.translator import get_translator_by_name
from arguments_processor import settings


class FileTranslator:
    default_open_mode = 'r+'

    code_mark = '```'
    paragraph_regexp = re.compile(r'^[a-zA-Z]+.*')

    def __init__(self, file_path):
        self.__translator = get_translator_by_name(settings.service)
        self.__file_path = file_path
        self.__line_processor = None
        self.file_contents_with_translation = []
        self.code_block = False

    def translate(self):
        lines = self.__translating_file.readlines()
        for counter, line in enumerate(lines):
            self.file_contents_with_translation.append(line)
            self.__line_processor = LineProcessor(line)
            self.code_block = not self.code_block if self.__line_processor.is_code_block_border() else self.code_block
            if self.line_have_to_be_translated():
                translated = self.__translator.request_translation(line)
                self.file_contents_with_translation.append('\n')
                self.file_contents_with_translation.append(translated)

                print('Processed: {percent}% ({counter} of {lines})'.format(percent=(counter / len(lines) * 100),
                                                                            counter=counter, lines=len(lines)))

        self.__write_translated_data_to_file()

    def line_have_to_be_translated(self):
        return self.__line_processor.line_can_be_translated and not self.code_block

    def __write_translated_data_to_file(self):
        self.__translating_file.seek(0)
        self.__translating_file.writelines(self.file_contents_with_translation)

    def __enter__(self):
        self.__translating_file = open(self.__file_path, self.default_open_mode)
        return self

    def __exit__(self, *args, **kwargs):
        self.__translating_file.close()
