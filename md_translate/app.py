from pathlib import Path
from typing import Sequence

from md_translate.file_translator import FileTranslator
from md_translate.files_worker import FilesWorker


class App:
    def process(self) -> None:
        files_to_process: Sequence[Path] = FilesWorker().md_files_list
        for file_name in files_to_process:
            with FileTranslator(file_name) as processing_file:
                processing_file.translate()
            print('Processed: {file_name}'.format(file_name=file_name))


def run() -> None:
    try:
        App().process()
        exit(0)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":
    run()
