import os
import unittest

from md_translate.exceptions import DirectoryNotFoundException
from md_translate.files_worker import FilesWorker


class TestFilesWorker(unittest.TestCase):
    test_data_folder = os.path.join('data', 'test_data')

    def test_folder_errors(self):
        with self.assertRaises(DirectoryNotFoundException):
            FilesWorker('not existing folder')
        with self.assertRaises(NotADirectoryError):
            FilesWorker(os.path.join(self.test_data_folder, 'not_a_folder'))
        with self.assertRaises(FileNotFoundError):
            FilesWorker(os.path.join(self.test_data_folder, 'folder_without_md_files'))
        self.assertListEqual(
            sorted(['first_file.md', 'second_file.md']),
            sorted(FilesWorker(os.path.join(self.test_data_folder, 'md_files_folder')).md_files_list)
        )
