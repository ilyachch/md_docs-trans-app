import json
from pathlib import Path
from contextlib import nullcontext as does_not_raise
import click
import pytest
from pydantic.v1 import BaseModel, ValidationError

from md_translate.settings import Settings
from md_translate.settings._settings_to_cli import (
    SettingsToCliField,
    build_cli_options_from_settings,
    wrap_command_with_options,
)
from md_translate.translators import GoogleTranslateProvider, Translator


class TestSettings(BaseModel):
    option_one: str = SettingsToCliField(
        click_option_name=["--option_one"],
        click_option_type=click.STRING,
        click_option_help="Help for option one",
        click_option_required=True,
    )

    option_two: int = SettingsToCliField(
        click_option_name=["--option_two"],
        click_option_type=click.INT,
        click_option_help="Help for option two",
        click_option_required=False,
        click_option_default=0,
    )


def test_SettingsToCliField():
    assert 'option_one' in TestSettings.__fields__
    assert 'option_two' in TestSettings.__fields__
    assert TestSettings.__fields__['option_one'].field_info.extra['click_option_name'] == [
        "--option_one"
    ]
    assert TestSettings.__fields__['option_two'].field_info.extra['click_option_name'] == [
        "--option_two"
    ]


def test_build_cli_options_from_settings():
    options = build_cli_options_from_settings(TestSettings)  # type: ignore
    assert len(options) == 2
    assert isinstance(options[0], click.Option)
    assert options[0].name == "option_one"
    assert options[1].name == "option_two"


def test_wrap_command_with_options():
    @wrap_command_with_options(TestSettings)  # type: ignore
    def command(**kwargs):
        pass

    assert command.__click_params__
    assert len(command.__click_params__) == 2
    assert isinstance(command.__click_params__[0], click.Option)
    assert command.__click_params__[0].name == "option_two"
    assert command.__click_params__[1].name == "option_one"


def test_settings_validator():
    with pytest.raises(ValidationError):
        Settings(
            path=Path('.'),
            from_lang='en',
            to_lang='ru',
            service='invalid_service',
            processes=1,
            new_file=False,
            ignore_cache=False,
            save_temp_on_complete=False,
            overwrite=False,
            verbose=0,
            drop_original=False,
        )


def test_settings_instantiate():
    settings = Settings.initiate(
        click_params={
            'path': Path('.'),
            'from_lang': 'en',
            'to_lang': 'ru',
            'service': Translator.google,
            'processes': 1,
            'new_file': False,
            'ignore_cache': False,
            'save_temp_on_complete': False,
            'overwrite': False,
            'verbose': 0,
            'drop_original': False,
        },
        config_file_path=None,
    )

    assert isinstance(settings, Settings)
    assert settings.from_lang == 'en'
    assert settings.to_lang == 'ru'
    assert settings.service == GoogleTranslateProvider
    assert settings.service_provider == GoogleTranslateProvider


def test_settings_initiate_with_unknown_option_in_click_params():
    with pytest.raises(ValueError):
        Settings.initiate(
            click_params={'path': Path('.'), 'unknown_option': 'value'}, config_file_path=None
        )


@pytest.mark.parametrize(
    "config_data, raises",
    [
        (
            {
                "processes": 1,
                "new_file": False,
                "ignore_cache": False,
                "save_temp_on_complete": False,
                "overwrite": False,
                "verbose": 0,
                "drop_original": False,
                "unknown_option": "value",
            },
            pytest.raises(ValueError),
        ),
        (
            {
                "processes": 1,
                "new_file": False,
                "ignore_cache": False,
                "save_temp_on_complete": False,
                "overwrite": False,
                "verbose": 0,
                "drop_original": False,
            },
            does_not_raise(),
        ),
    ],
)
def test_settings_initiate_with_unknown_option_in_config_file(config_data, raises, tmp_path):
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    with raises:
        Settings.initiate(
            click_params={
                "path": ".",
                "from_lang": "en",
                "to_lang": "ru",
                "service": Translator.google,
            },
            config_file_path=config_file,
        )


def test_dump_settings(capsys):
    settings = Settings(
        path=Path('.'),
        from_lang='en',
        to_lang='ru',
        service=Translator.google,
        processes=1,
        new_file=False,
        ignore_cache=False,
        save_temp_on_complete=False,
        overwrite=False,
        verbose=0,
        drop_original=False,
    )
    settings.dump_settings()
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "processes": 1,
        "new_file": False,
        "ignore_cache": False,
        "save_temp_on_complete": False,
        "overwrite": False,
        "verbose": 0,
        "drop_original": False,
        "deepl_api_key": None,
    }
