import pathlib

from md_translate.exceptions import DirectoryNotFoundException
from md_translate.file_translator import FileTranslator


class FilesWorker:
    def __init__(self, folder_to_process):
        self.__folder_to_process: pathlib.Path = pathlib.Path(folder_to_process)
        self.__validate_folder()
        self.md_files_list: list = self.__get_md_files_list()

    def __validate_folder(self):
        if not self.__folder_to_process.exists():
            raise DirectoryNotFoundException('No such folder: {}!'.format(self.__folder_to_process))
        if not self.__folder_to_process.is_dir():
            raise NotADirectoryError('With selected path provided a file, not a folder!')

    def __get_md_files_list(self) -> list:
        md_files_list = []
        for link in self.__folder_to_process.iterdir():
            if link.suffix == '.md':
                md_files_list.append(link.name)
        if len(md_files_list) == 0:
            raise FileNotFoundError('There are no MD files found with provided path!')
        return md_files_list

    def process(self):
        for file_name in self.md_files_list:
            md_file_abs_path = self.__folder_to_process.joinpath(file_name)
            with FileTranslator(md_file_abs_path) as processing_file:
                processing_file.translate()
            print('Processed: {file_name}'.format(file_name=file_name))
