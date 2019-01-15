import re

from md_translate.translator import Translator


class FileTranslator:
    default_open_mode = 'r+'

    code_mark = '```'
    paragraph_regexp = re.compile(r'^[a-zA-Z]+.*')

    def __init__(self, file_path):
        self.__translator = Translator()
        self.__file_path = file_path
        self.file_contents_with_translation = []
        self.code_block = False

    def translate(self):
        lines = self.__translating_file.readlines()
        for counter, line in enumerate(lines):
            self.file_contents_with_translation.append(line)
            self.__check_line_for_code_mark(line)
            if self.line_should_be_translated(line):
                translated = self.__translator.request_translation(line)
                self.file_contents_with_translation.append('\n')
                self.file_contents_with_translation.append(translated)

                print('Processed: {percent}% ({counter} of {lines})'.format(percent=(counter/len(lines)*100), counter=counter, lines=len(lines)))

        self.__write_translated_data_to_file()

    def __write_translated_data_to_file(self):
        self.__translating_file.seek(0)
        self.__translating_file.writelines(self.file_contents_with_translation)

    def line_should_be_translated(self, line):
        return not (self.__is_single_line_code(line) or
                    self.__not_paragraph(line) or
                    self.code_block)

    def __check_line_for_code_mark(self, line):
        if line.startswith(self.code_mark) and not line.endswith(self.code_mark):
            self.code_block = not self.code_block

    def __is_single_line_code(self, line):
        if line.startswith(self.code_mark) and line.endswith(self.code_mark) and len(line) > 3:
            return True
        return False

    def __not_paragraph(self, line):
        if not self.paragraph_regexp.match(line):
            return True
        return False

    def __enter__(self):
        self.__translating_file = open(self.__file_path, self.default_open_mode)
        return self

    def __exit__(self, *args, **kwargs):
        self.__translating_file.close()
