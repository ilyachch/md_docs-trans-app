from pathlib import Path
from typing import List, Union

import click

from md_translate.document import MarkdownDocument
from md_translate.providers import TRANSLATOR_BY_SERVICE_NAME


@click.command()
@click.argument(
    'path',
    type=click.Path(exists=True, path_type=Path),
    # help='Path to folder or file to process.',
    required=True,
)
@click.option(
    '--from-lang',
    type=click.STRING,
    help='Source language code',
    required=True,
)
@click.option(
    '--to-lang',
    type=click.STRING,
    help='Target language code',
    required=True,
)
@click.option(
    '--service',
    type=click.Choice(list(TRANSLATOR_BY_SERVICE_NAME.keys())),
    help='Translating service',
    required=True,
)
@click.option(
    '--new-file',
    is_flag=True,
    default=False,
    help='Create new file with translated content',
)
@click.option('--clear', is_flag=True, help='Start from scratch.')
def main(
    path: Union[Path, List[Path]],
    from_lang: str,
    to_lang: str,
    service: str,
    new_file: bool,
    clear: bool,
) -> None:
    if not isinstance(path, list):
        path = [
            path,
        ]
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

    translation_provider = TRANSLATOR_BY_SERVICE_NAME[service]()
    for file_to_process in files_to_process:
        click.echo('Processing file: {}'.format(file_to_process.name))
        document = MarkdownDocument.from_file(file_to_process, force_new=clear)
        document.translate(translation_provider, from_lang, to_lang, new_file=new_file)
        click.echo('Processed file: {}'.format(file_to_process.name))
    click.echo('Done')
    exit(0)


if __name__ == "__main__":
    main()
