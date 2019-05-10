import os
import unittest
from pathlib import Path

from md_translate.exceptions import DirectoryNotFoundException
from md_translate.files_worker import FilesWorker


class TestFilesWorker(unittest.TestCase):
    test_data_folder = Path('data/test_data')

    def test_folder_errors(self):
        with self.assertRaises(DirectoryNotFoundException):
            FilesWorker('not existing folder')
        with self.assertRaises(NotADirectoryError):
            FilesWorker(self.test_data_folder.joinpath('not_a_folder'))
        with self.assertRaises(FileNotFoundError):
            FilesWorker(self.test_data_folder.joinpath('folder_without_md_files'))
        self.assertListEqual(
            sorted(['first_file.md', 'second_file.md']),
            sorted(FilesWorker(self.test_data_folder.joinpath('md_files_folder')).md_files_list)
        )
