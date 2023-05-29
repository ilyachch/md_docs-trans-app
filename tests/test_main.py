from copy import copy
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest
from click import Command
from click.testing import CliRunner

import md_translate.main as md_translate_main
from md_translate.settings import Settings
from md_translate.translators.google import GoogleTranslateProvider


class FakeApplication:
    _SETTINGS: Settings
    def __init__(self):
        self._settings = self._SETTINGS

    def run(self) -> int:
        return 0

    @classmethod
    def with_fake_settings(cls, settings):
        cls_ = copy(cls)
        cls_._SETTINGS = settings
        return cls_


@pytest.fixture
def fake_application(test_settings):
    FakeApp = FakeApplication.with_fake_settings(test_settings)
    with patch.object(md_translate_main, 'Application', FakeApp):
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
        assert fake_application._settings.path == Path('tests')
        assert fake_application._settings.from_lang == 'en'
        assert fake_application._settings.to_lang == 'ru'
        assert fake_application._settings.service is GoogleTranslateProvider
        assert fake_application._settings.processes == 1
        assert fake_application._settings.new_file is False
        assert fake_application._settings.ignore_cache == False
        assert fake_application._settings.save_temp_on_complete == False
        assert fake_application._settings.overwrite == False
        assert fake_application._settings.verbose == 0
