from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest
from click import Command
from click.testing import CliRunner

import md_translate.main as md_translate_main
from md_translate.settings import settings
from md_translate.translators.google import GoogleTranslateProvider


class FakeApplication:
    def __init__(self, settings_obj):
        self._settings = settings_obj

    def run(self) -> int:
        return 0


@pytest.fixture
def fake_application():
    with patch.object(md_translate_main, 'Application', FakeApplication):
        yield


class TestMain:
    @pytest.mark.parametrize(
        'params, exit_code',
        (
            ([], 2),
            (['-F', 'en', '-T', 'ru', '-P', 'google', 'tests'], 0),
        ),
    )
    def test_params(self, params, exit_code, fake_application):
        runner = CliRunner()
        result = runner.invoke(cast(Command, md_translate_main.main), params)
        assert result.exit_code == exit_code


class TestSettings:
    def test_settings(self, fake_application):
        runner = CliRunner()
        runner.invoke(
            cast(Command, md_translate_main.main),
            ['-F', 'en', '-T', 'ru', '-P', 'google', 'tests'],
        )
        assert settings.path == Path('tests')
        assert settings.from_lang == 'en'
        assert settings.to_lang == 'ru'
        assert settings.service is GoogleTranslateProvider
        assert settings.service_host is None
        assert settings.processes == 1
        assert settings.webdriver is None
        assert settings.new_file is False
        assert settings.ignore_cache == False
        assert settings.save_temp_on_complete == False
        assert settings.overwrite == False
        assert settings.verbose == 0
