from pathlib import Path
from typing import Sequence

from md_translate.arguments_processor import ArgumentsProcessor
from md_translate.exceptions import ObjectNotFoundException, FileIsNotMarkdown


class FilesWorker:
    def __init__(self, settings: ArgumentsProcessor):
        self.settings: ArgumentsProcessor = settings
        self.single_file: bool = False
        self.object_to_process: Path = self.settings.path
        self.__check_for_single_obj()
        self.__validate_folder()
        self.md_files_list: Sequence[Path] = self.__get_md_files_list()

    def __check_for_single_obj(self) -> None:
        if self.object_to_process.is_file() and self.object_to_process.suffix == '.md':
            self.single_file = True
        elif self.object_to_process.is_file():
            raise FileIsNotMarkdown(self.object_to_process)

    def __validate_folder(self) -> None:
        if not self.object_to_process.exists():
            raise ObjectNotFoundException(self.object_to_process)

    def __get_md_files_list(self) -> Sequence[Path]:
        md_files_list: list = []
        if self.single_file:
            md_files_list.append(self.object_to_process)
        else:
            for link in self.object_to_process.iterdir():
                if link.suffix == '.md':
                    md_files_list.append(link)
        if len(md_files_list) == 0:
            raise FileNotFoundError('There are no MD files found with provided path!')

        return md_files_list
