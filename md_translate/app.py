import logging
from pathlib import Path
from typing import List, Optional, Union

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
    '--service-host',
    type=click.STRING,
    help='Translating service host override',
)
@click.option(
    '-W',
    '--webdriver',
    type=click.Path(exists=True, path_type=Path),
    help='Path to webdriver',
    envvar='WEBDRIVER_PATH',
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
    service_host: Optional[str],
    webdriver: Optional[Path],
    new_file: bool,
    ignore_cache: bool,
    save_temp_on_complete: bool,
    overwrite: bool,
    verbose: int,
) -> None:
    _set_logging_level(verbose)
    files_to_process = get_files_to_process(path)
    translation_provider = TRANSLATOR_BY_SERVICE_NAME[service](
        host=service_host or None,
        webdriver_path=webdriver or None,
        from_language=from_lang,
        to_language=to_lang,
    )
    for file_num, file_to_process in enumerate(files_to_process, start=1):
        document = MarkdownDocument.from_file(file_to_process, ignore_cache=ignore_cache)
        click.echo(f'Processing file {file_num}/{len(files_to_process)}: {file_to_process.name}')
        if not document.should_be_translated(new_file=new_file, overwrite=overwrite):
            logging.info('Skipping file: %s. Already translated', file_to_process.name)
            continue
        with translation_provider as provider:
            try:
                document.translate(provider)
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
    elif verbose == 2:
        logging.basicConfig(level=logging.INFO)
    elif verbose == 3:
        logging.basicConfig(level=logging.INFO)
    elif verbose == 4:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)


def get_files_to_process(path: Union[List[Path], Path]) -> List[Path]:
    if not isinstance(path, list):
        path = [
            path,
        ]
    files_to_process = []
    for path_to_process in path:
        if not path_to_process.exists():
            raise click.ClickException(f'Path not found: {path_to_process}')
        if path_to_process.is_file():
            logger.debug('Found file: %s', path_to_process)
            files_to_process.append(path_to_process)
        else:
            found_files = path_to_process.glob('**/*.md')
            for found_file in found_files:
                logger.debug('Found file: %s', found_file)
                files_to_process.append(found_file)

    source_files = [
        file_to_process
        for file_to_process in files_to_process
        if '_translated' not in file_to_process.name
    ]

    logger.info('Found %s files to process: %s', len(source_files), source_files)
    return source_files


if __name__ == "__main__":
    main()
