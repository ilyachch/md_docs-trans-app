import unittest
from pathlib import Path

from md_translate.exceptions import ObjectNotFoundException, FileIsNotMarkdown
from md_translate.files_worker import FilesWorker

TEST_FIRST_FILE = 'tests/test_data/md_files_folder/first_file.md'
TEST_SECOND_FILE = 'tests/test_data/md_files_folder/second_file.md'

class TestFilesWorker(unittest.TestCase):
    def test_folder_errors(self):
        class SettingsMock:
            def __init__(self, path):
                self.path = Path('tests/test_data').joinpath(path)

        with self.assertRaises(ObjectNotFoundException):
            FilesWorker(SettingsMock('not existing folder'))
        with self.assertRaises(FileNotFoundError):
            FilesWorker(SettingsMock('folder_without_md_files'))
        with self.assertRaises(FileIsNotMarkdown):
            FilesWorker(SettingsMock('not_a_folder'))
        with self.assertRaises(FileIsNotMarkdown):
            FilesWorker(SettingsMock('not_markdown_file.txt'))

    def test_multiple_objects(self):
        class MockedSettings:
            path = Path('tests/test_data/md_files_folder')

        file_worker_object = FilesWorker(MockedSettings())
        self.assertFalse(file_worker_object.single_file)
        self.assertListEqual(
            sorted(file_worker_object.md_files_list),
            sorted([
                Path(TEST_FIRST_FILE),
                Path(TEST_SECOND_FILE)
            ]),
        )

    def test_single_object(self):
        class MockedSettings:
            path = Path(TEST_FIRST_FILE)

        file_worker_object = FilesWorker(MockedSettings())
        self.assertTrue(file_worker_object)
        self.assertEqual(
            file_worker_object.md_files_list,
            [Path(TEST_FIRST_FILE)]
        )
