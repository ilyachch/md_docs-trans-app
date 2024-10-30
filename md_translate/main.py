from pathlib import Path
from typing import Any

import click

from md_translate.application import Application
from md_translate.settings import Settings, wrap_command_with_options


@click.command()
@click.argument(
    'path',
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@wrap_command_with_options(Settings)
def main(
    **cli_arguments: Any,
) -> None:
    dump_config = cli_arguments.pop('dump_config', False)
    config_file = cli_arguments.pop('config', None)
    settings = Settings.initiate(click_params=cli_arguments, config_file_path=config_file)
    if dump_config:
        settings.dump_settings()
    exit(Application(settings).run())


if __name__ == "__main__":
    main()  # pragma: no cover
