from pathlib import Path

import pytest

from md_translate.exceptions import ObjectNotFoundException, FileIsNotMarkdown
from md_translate.files_worker import FilesWorker

TEST_FIRST_FILE = 'tests/test_data/md_files_folder/first_file.md'
TEST_SECOND_FILE = 'tests/test_data/md_files_folder/second_file.md'


class SettingsMock:
    def __init__(self, path):
        self.path = Path('tests/test_data').joinpath(path)


class TestFilesWorker:
    @pytest.mark.parametrize('path, err', [
        ['not existing folder', ObjectNotFoundException],
        ['folder_without_md_files', FileNotFoundError],
        ['not_a_folder', FileIsNotMarkdown],
        ['not_markdown_file.txt', FileIsNotMarkdown],
    ])
    def test_folder_errors(self, path, err):
        with pytest.raises(err):
            FilesWorker(SettingsMock(path)).get_md_files()

    def test_multiple_objects(self):
        file_worker_object = FilesWorker(SettingsMock('md_files_folder'))
        assert file_worker_object.single_file == False
        assert sorted(file_worker_object.get_md_files()) == [Path(TEST_FIRST_FILE), Path(TEST_SECOND_FILE)]

    def test_single_object(self):
        file_worker_object = FilesWorker(SettingsMock('md_files_folder/first_file.md'))
        assert file_worker_object.single_file == True
        assert file_worker_object.get_md_files() == [Path(TEST_FIRST_FILE)]
