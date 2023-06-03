import logging
import multiprocessing
from pathlib import Path
from typing import TYPE_CHECKING

import click

from md_translate.document import MarkdownDocument
from md_translate.exceptions import NoMdFilesFound, NoTargetFileFound

if TYPE_CHECKING:
    from md_translate.settings import Settings


class Application:
    def __init__(self, settings: 'Settings'):
        self._settings = settings
        self._logger = logging.getLogger(__name__)

    def run(self) -> int:
        self._set_logging_level()
        if self._settings.processes == 1:
            self.run_single_process()
            return 0
        else:
            self.run_multiple_processes()
            return 0

    def run_single_process(self) -> None:
        files_to_process = self._get_files_to_process()
        for file_to_process in files_to_process:
            self.process_file(file_to_process)

    def run_multiple_processes(self) -> None:
        files_to_process = self._get_files_to_process()
        with multiprocessing.Pool(self._settings.processes) as pool:
            pool.starmap(
                self.process_file,
                [(file_to_process,) for file_to_process in files_to_process],
            )

    def _set_logging_level(self) -> None:
        level_int_to_name = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.INFO,
            4: logging.DEBUG,
        }
        logging_level = level_int_to_name.get(self._settings.verbose, logging.DEBUG)
        logging.basicConfig(level=logging_level)
        LOGGER_NAMES_TO_DISABLE = [
            'selenium',
            'urllib3',
            'WDM',
        ]
        for logger_name in LOGGER_NAMES_TO_DISABLE:
            logging.getLogger(logger_name).setLevel(logging.CRITICAL)

    def _get_files_to_process(self) -> list[Path]:
        files_to_process = self._aggregate_files_to_process()
        source_files = [
            file_to_process
            for file_to_process in files_to_process
            if '_translated' not in file_to_process.name
        ]

        if not source_files:
            raise NoMdFilesFound('No markdown files found to process')

        common_path_part = Path(
            *(
                part
                for part in source_files[0].parts
                if all(part in file.parts for file in source_files)
            )
        )

        self._logger.info(
            'Found %s files to process: %s',
            len(source_files),
            ', '.join([str(f.relative_to(common_path_part)) for f in source_files]),
        )
        return source_files

    def _aggregate_files_to_process(self) -> list[Path]:
        paths = self._settings.path
        files_to_process = []
        for path_to_process in paths:
            if not path_to_process.exists():
                raise NoTargetFileFound(f'Path not found: {path_to_process}')
            if path_to_process.is_file():
                self._logger.debug('Found file: %s', path_to_process)
                files_to_process.append(path_to_process)
            else:
                found_files = path_to_process.glob('**/*.md')
                for found_file in found_files:
                    self._logger.debug('Found file: %s', found_file)
                    files_to_process.append(found_file)
        return files_to_process

    def process_file(self, file_to_process: Path) -> None:
        translation_provider = self._settings.service_provider(self._settings)
        self._logger.info('Processing file: %s', file_to_process)
        try:
            document = MarkdownDocument.from_file(
                file_to_process,
                settings=self._settings,
            )
        except Exception as e:
            self._logger.error('Error processing file: %s', file_to_process)
            self._logger.exception(e)
            return
        if not document.should_be_translated():
            self._logger.info('Skipping file: %s. Already translated', file_to_process.name)
            return
        with translation_provider as provider:
            try:
                document.translate(provider)
            except Exception as e:
                self._logger.error('Error while translating file: %s', file_to_process.name)
                self._logger.exception(e)
                return
        document.write()
        click.echo('Processed file: {}'.format(file_to_process.name))
