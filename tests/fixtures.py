from pathlib import Path
from typing import Union, Type, Optional

import pytest

from md_translate.translators import BaseTranslator


class SettingsTest:
    path: Optional[Union[Path, list[Path]]] = None
    from_lang: Optional[str] = None
    to_lang: Optional[str] = None
    service: Optional[Type[BaseTranslator]] = None
    processes: int = 1
    new_file: bool = False
    ignore_cache: bool = False
    save_temp_on_complete: bool = False
    overwrite: bool = False
    verbose: int = 0
    drop_original: bool = False


@pytest.fixture
def test_settings():
    return SettingsTest()


@pytest.fixture
def test_settings_raw():
    return SettingsTest
