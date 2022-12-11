from pathlib import Path
from typing import Any, Optional, Type, Union

from translators import PTranslator, Translator
from translators._base import TranslationProvider


class Settings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_option(self, option_name: str, value: Any):
        setattr(self, f'_{option_name}', value)

    @property
    def path(self) -> Union[Path, list[Path]]:
        return getattr(self, '_path')

    @property
    def from_lang(self) -> str:
        return getattr(self, '_from_lang')

    @property
    def to_lang(self) -> str:
        return getattr(self, '_to_lang')

    @property
    def service(self) -> Type[PTranslator]:
        return getattr(self, '_service').value

    @property
    def service_host(self) -> Optional[str]:
        return getattr(self, '_service_host')

    @property
    def processes(self) -> int:
        return getattr(self, '_processes')

    @property
    def webdriver(self) -> Optional[Path]:
        return getattr(self, '_webdriver')

    @property
    def new_file(self) -> bool:
        return getattr(self, '_new_file')

    @property
    def ignore_cache(self) -> bool:
        return getattr(self, '_ignore_cache')

    @property
    def save_temp_on_complete(self) -> bool:
        return getattr(self, '_save_temp_on_complete')

    @property
    def overwrite(self) -> bool:
        return getattr(self, '_overwrite')

    @property
    def verbose(self) -> int:
        return getattr(self, '_verbose')


settings = Settings()
