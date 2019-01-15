import os

from md_translate.exceptions import DirectoryNotFoundException
from md_translate.file_translator import FileTranslator


class FilesWorker:
    def __init__(self, folder_to_process):
        self.__folder_to_process = folder_to_process
        self.__validate_folder()
        self.md_files_list = self.__get_md_files_list()

    def __validate_folder(self):
        if not os.path.exists(self.__folder_to_process):
            raise DirectoryNotFoundException('No such folder: {}!'.format(self.__folder_to_process))
        if not os.path.isdir(self.__folder_to_process):
            raise NotADirectoryError('With selected path provided a file, not a folder!')

    def __get_md_files_list(self):
        md_files_list = []
        for link in os.listdir(self.__folder_to_process):
            if link.endswith('.md'):
                md_files_list.append(link)
        if len(md_files_list) == 0:
            raise FileNotFoundError('There are no MD files found with provided path!')
        return md_files_list

    def process(self):
        for file_name in self.md_files_list:
            with FileTranslator(os.path.join(self.__folder_to_process, file_name)) as processing_file:
                processing_file.translate()
            print('Processed: {file_name}'.format(file_name=file_name))
