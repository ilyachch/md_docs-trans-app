import pathlib

from md_translate.exceptions import ObjectNotFoundException, FileIsNotMarkdown
from typing import Sequence


class FilesWorker:
    def __init__(self, settings):
        self.settings = settings
        self.single_file = False
        self.object_to_process: pathlib.Path = self.settings.path
        self.__check_for_single_obj()
        self.__validate_folder()
        self.md_files_list: Sequence[pathlib.Path] = self.__get_md_files_list()

    def __check_for_single_obj(self):
        if self.object_to_process.is_file() and self.object_to_process.suffix == '.md':
            self.single_file = True
        elif self.object_to_process.is_file():
            raise FileIsNotMarkdown('{} is not a Markdown file!'.format(self.object_to_process))

    def __validate_folder(self):
        if not self.object_to_process.exists():
            raise ObjectNotFoundException('{} not found'.format(self.object_to_process))

    def __get_md_files_list(self) -> Sequence[pathlib.Path]:
        md_files_list = []
        if self.single_file:
            md_files_list.append(self.object_to_process)
        else:
            for link in self.object_to_process.iterdir():
                if link.suffix == '.md':
                    md_files_list.append(link)
            if len(md_files_list) == 0:
                raise FileNotFoundError('There are no MD files found with provided path!')
        return md_files_list
