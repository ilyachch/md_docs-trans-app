import unittest
from pathlib import Path

from md_translate.exceptions import DirectoryNotFoundException
from md_translate.files_worker import FilesWorker


class TestFilesWorker(unittest.TestCase):
    class SettingsMock:
        _path = Path('tests/test_data')

        def __init__(self, path):
            self.path = self._path.joinpath(path)

    def test_folder_errors(self):
        with self.assertRaises(DirectoryNotFoundException):
            FilesWorker(self.SettingsMock('not existing folder'))
        with self.assertRaises(NotADirectoryError):
            FilesWorker(self.SettingsMock('not_a_folder'))
        with self.assertRaises(FileNotFoundError):
            FilesWorker(self.SettingsMock('folder_without_md_files'))
        self.assertListEqual(
            sorted(['first_file.md', 'second_file.md']),
            sorted(FilesWorker(self.SettingsMock('md_files_folder')).md_files_list)
        )
