import unittest
from pathlib import Path

from md_translate.exceptions import ObjectNotFoundException, FileIsNotMarkdown
from md_translate.files_worker import FilesWorker

TEST_FIRST_FILE = 'tests/test_data/md_files_folder/first_file.md'
TEST_SECOND_FILE = 'tests/test_data/md_files_folder/second_file.md'

class TestFilesWorker(unittest.TestCase):
    def test_folder_errors(self):
        from md_translate import settings
        class SettingsMock:
            def __init__(self, path):
                self.path = Path('tests/test_data').joinpath(path)
        with self.assertRaises(ObjectNotFoundException):
            settings.settings = SettingsMock('not existing folder')
            FilesWorker()
        with self.assertRaises(FileNotFoundError):
            settings.settings = SettingsMock('folder_without_md_files')
            FilesWorker()
        with self.assertRaises(FileIsNotMarkdown):
            settings.settings = SettingsMock('not_a_folder')
            FilesWorker()
        with self.assertRaises(FileIsNotMarkdown):
            settings.settings = SettingsMock('not_markdown_file.txt')
            FilesWorker()

    def test_multiple_objects(self):
        class MockedSettings:
            path = Path('tests/test_data/md_files_folder')

        from md_translate import settings
        settings.settings = MockedSettings()
        file_worker_object = FilesWorker()
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
        from md_translate import settings
        settings.settings = MockedSettings()
        file_worker_object = FilesWorker()
        self.assertTrue(file_worker_object)
        self.assertEqual(
            file_worker_object.md_files_list,
            [Path(TEST_FIRST_FILE)]
        )
