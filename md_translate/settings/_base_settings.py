import json
from pathlib import Path
from typing import Any, ClassVar, Optional, Type, Union, cast

import click
from pydantic import BaseModel

from md_translate.settings._settings_to_cli import SettingsToCliField
from md_translate.translators import BaseTranslator, Translator


class Settings(BaseModel):
    path: Union[Path, list[Path]]
    from_lang: str = SettingsToCliField(
        click_option_name=['-F', '--from-lang'],
        click_option_type=click.STRING,
        click_option_help='Source language code',
        click_option_required=True,
    )
    to_lang: str = SettingsToCliField(
        click_option_name=['-T', '--to-lang'],
        click_option_type=click.STRING,
        click_option_help='Target language code',
        click_option_required=True,
    )
    service: Translator = SettingsToCliField(
        click_option_name=['-P', '--service'],
        click_option_type=click.Choice(Translator.__members__),  # type: ignore
        click_option_callback=lambda ctx, param, value: Translator[value],
        click_option_help='Translating service',
        click_option_required=True,
    )
    processes: int = SettingsToCliField(
        1,
        click_option_name=['-X', '--processes'],
        click_option_type=click.INT,
        click_option_help='Number of processes to use',
        click_option_default=1,
    )
    new_file: bool = SettingsToCliField(
        False,
        click_option_name=['-N', '--new-file'],
        click_option_type=click.BOOL,
        click_option_is_flag=True,
        click_option_help='Create new file with translated text',
        click_option_default=False,
    )
    ignore_cache: bool = SettingsToCliField(
        False,
        click_option_name=['-I', '--ignore-cache'],
        click_option_is_flag=True,
        click_option_help='Ignore cache',
    )
    save_temp_on_complete: bool = SettingsToCliField(
        False,
        click_option_name=['-S', '--save-temp-on-complete'],
        click_option_is_flag=True,
        click_option_help='Save temporary files on complete',
    )
    overwrite: bool = SettingsToCliField(
        False,
        click_option_name=['-O', '--overwrite'],
        click_option_is_flag=True,
        click_option_help='Overwrite original files',
    )
    verbose: int = SettingsToCliField(
        0,
        click_option_name=['-v', '--verbose'],
        click_option_count=True,
        click_option_help='Verbosity level',
    )
    drop_original: bool = SettingsToCliField(
        False,
        click_option_name=['-D', '--drop-original'],
        click_option_is_flag=True,
        click_option_help='Drop original files',
    )

    DEFAULT_CONFIG_FILE_NAME: ClassVar[Path] = Path(
        '~/.config/md_translate/settings.json'
    ).expanduser()

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True

    @property
    def service_provider(self) -> Type[BaseTranslator]:
        return cast(Type[BaseTranslator], self.service)

    @classmethod
    def initiate(
        cls,
        *,
        click_params: dict[str, Any],
        config_file_path: Optional[Path] = None,
    ) -> 'Settings':
        not_default_params = cls.__get_not_default_params(click_params)
        params_from_config_file = cls.__get_params_from_config_file(config_file_path)
        params = {**params_from_config_file, **not_default_params}
        clear_params = {k: v for k, v in params.items() if v is not None}
        return cls(**clear_params)

    @classmethod
    def __get_params_from_config_file(
        cls,
        config_file_path: Optional[Path] = None,
    ) -> dict[str, Any]:
        params = {}
        if config_file_path is None:
            config_file_path = cls.DEFAULT_CONFIG_FILE_NAME
        if not config_file_path.exists():
            return {}
        file_data = json.loads(config_file_path.read_text())
        for option_name, value in file_data.items():
            if option_name not in cls.__fields__:
                raise ValueError(f'Unknown option: {option_name}')
            params[option_name] = value
        return params

    @classmethod
    def __get_not_default_params(cls, params: dict[str, Any]) -> dict[str, Any]:
        not_default_params = {}
        for option_name, value in params.items():
            if option_name not in cls.__fields__:
                raise ValueError(f'Unknown option: {option_name}')
            if value != cls.__fields__[option_name].default:
                not_default_params[option_name] = value
        return not_default_params

    def dump_settings(self) -> None:
        print(self.json(indent=4, exclude={'path', 'from_lang', 'to_lang', 'service'}))
