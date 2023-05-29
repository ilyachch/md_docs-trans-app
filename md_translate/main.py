from pathlib import Path
from typing import Any

import click

from md_translate.application import Application
from md_translate.settings import Settings, wrap_command_with_options
from md_translate.translators import Translator


@click.command()
@click.argument(
    'path',
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@wrap_command_with_options(Settings)
def main(
    **kwargs: Any,
) -> None:
    dump_config = kwargs.pop('dump_config', False)
    # cli_params = get_not_default_params()
    settings = Settings.initiate(click_params=cli_params, config_file_path=kwargs.pop('config'))
    if dump_config:
        settings.dump_settings()
    exit_code = Application(settings).run()
    exit(exit_code)


if __name__ == "__main__":
    main()  # pragma: no cover
