import logging
from pathlib import Path
from typing import List, Union

import click

from md_translate.document.document import MarkdownDocument
from md_translate.translators import TRANSLATOR_BY_SERVICE_NAME

logger = logging.getLogger(__name__)


@click.command()
@click.argument(
    'path',
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option(
    '-F',
    '--from-lang',
    type=click.STRING,
    help='Source language code',
    required=True,
)
@click.option(
    '-T',
    '--to-lang',
    type=click.STRING,
    help='Target language code',
    required=True,
)
@click.option(
    '-P',
    '--service',
    type=click.Choice(list(TRANSLATOR_BY_SERVICE_NAME.keys())),
    help='Translating service',
    required=True,
)
@click.option(
    '-N',
    '--new-file',
    is_flag=True,
    default=False,
    help='Create new file with translated content',
)
@click.option(
    '-I',
    '--ignore-cache',
    is_flag=True,
    help='Ignore cache',
)
@click.option(
    '-S',
    '--save-temp-on-complete',
    is_flag=True,
    help='Save temp files on complete.',
)
@click.option(
    '-O',
    '--overwrite',
    is_flag=True,
    help='Overwrite existing files.',
)
@click.option(
    '-v',
    '--verbose',
    count=True,
)
def main(
    path: Union[Path, List[Path]],
    from_lang: str,
    to_lang: str,
    service: str,
    new_file: bool,
    clear: bool,
    save_temp_on_complete: bool,
    overwrite: bool,
    verbose: int,
) -> None:
    _set_logging_level(verbose)
    if not isinstance(path, list):
        path = [
            path,
        ]
    files_to_process = _get_files_to_process(path)
    logging.info('Found %s files to process', len(files_to_process))
    logging.debug('Files to process: %s', files_to_process)
    translation_provider = TRANSLATOR_BY_SERVICE_NAME[service]()
    for file_to_process in files_to_process:
        document = MarkdownDocument.from_file(file_to_process, ignore_cache=clear)
        click.echo('Processing file: {}'.format(file_to_process.name))
        if not document.should_be_translated(new_file=new_file, overwrite=overwrite):
            logging.info('Skipping file: %s. Already translated', file_to_process.name)
            continue
        with translation_provider as provider:
            try:
                document.translate(provider, from_lang, to_lang)
            except Exception as e:
                logging.error('Error while translating file: %s', file_to_process.name)
                logging.exception(e)
                continue
        document.write(new_file=new_file, save_temp_on_complete=save_temp_on_complete)
        click.echo('Processed file: {}'.format(file_to_process.name))
    click.echo('Done')
    exit(0)


def _set_logging_level(verbose: int) -> None:
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)


def _get_files_to_process(path: List[Path]) -> List[Path]:
    files_to_process = []
    for path_to_process in path:
        if not path_to_process.exists():
            raise click.ClickException(f'Path not found: {path_to_process}')
        if path_to_process.is_file():
            click.echo('Found file: {}'.format(path_to_process.name))
            files_to_process.append(path_to_process)
        else:
            found_files = path_to_process.glob('*.md')
            for found_file in found_files:
                click.echo('Found file: {}'.format(found_file.name))
                files_to_process.append(found_file)
    return files_to_process


if __name__ == "__main__":
    main()
