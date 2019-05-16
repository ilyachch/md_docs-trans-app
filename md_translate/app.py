from pathlib import Path
from typing import Sequence

from md_translate.arguments_processor import ArgumentsProcessor
from md_translate.exceptions import MdTranslateBaseException
from md_translate.file_translator import FileTranslator
from md_translate.files_worker import FilesWorker


class App:
    def __init__(self):
        self.settings: ArgumentsProcessor = ArgumentsProcessor()
        self.__validate_setup()

    def __validate_setup(self) -> None:
        try:
            self.settings.validate_arguments()
        except MdTranslateBaseException as err:
            print(err.get_message())
            exit(1)

    def process(self):
        files_to_process: Sequence[Path] = FilesWorker(self.settings).md_files_list
        for file_name in files_to_process:
            with FileTranslator(self.settings, file_name) as processing_file:
                processing_file.translate()
            print('Processed: {file_name}'.format(file_name=file_name))


def main():
    try:
        App().process()
        exit(0)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":
    main()
