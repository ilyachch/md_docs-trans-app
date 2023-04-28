from pathlib import Path
from typing import Any

import click

from md_translate.application import Application
from md_translate.settings import settings
from md_translate.translators import Translator


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
    type=click.Choice(Translator.__members__),  # type: ignore
    callback=lambda ctx, param, value: Translator[value],
    help='Translating service',
    required=True,
)
@click.option(
    '-X',
    '--processes',
    type=click.INT,
    help='Number of processes to use',
    default=1,
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
    '-D',
    '--drop-original',
    is_flag=True,
    help='Drop original lines after translation.',
)
@click.option(
    '-v',
    '--verbose',
    count=True,
)
@click.option(
    '--config',
    type=click.Path(exists=True, path_type=Path),
    help='Path to config file',
)
@click.option(
    '--dump-config',
    is_flag=True,
    help='Dump config',
)
def main(
    **kwargs: Any,
) -> None:
    dump_config = kwargs.pop('dump_config', False)
    settings.update_from_config(kwargs.pop('config'))
    for key, value in kwargs.items():
        settings.set_option(key, value)
    if dump_config:
        settings.dump()
    exit_code = Application(settings).run()
    exit(exit_code)


if __name__ == "__main__":
    main()  # pragma: no cover
