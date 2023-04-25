import pytest

from md_translate.settings import SettingsProtocol


class SettingsTest(SettingsProtocol):
    path = None
    from_lang = None
    to_lang = None
    service = None
    service_host = None
    processes = 1
    new_file = False
    ignore_cache = False
    save_temp_on_complete = False
    overwrite = False
    verbose = False
    drop_original = False

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture
def settings():
    return SettingsTest()
