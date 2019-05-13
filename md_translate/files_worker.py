import pathlib

from md_translate.exceptions import DirectoryNotFoundException


class FilesWorker:
    def __init__(self, settings):
        self.settings = settings
        self.__folder_to_process: pathlib.Path = pathlib.Path(self.settings.path)
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

    def get_files_to_translate(self):
        files_to_translate = [self.__folder_to_process.joinpath(file_name) for file_name in self.md_files_list]
        return files_to_translate
