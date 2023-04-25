from pathlib import Path
from typing import Protocol, Union, Type, Optional, Any

from translators import BaseTranslator


class SettingsProtocol(Protocol):
    path: Union[Path, list[Path]]
    from_lang: str
    to_lang: str
    service: Type[BaseTranslator]
    service_host: Optional[str]
    processes: int
    webdriver: Optional[Path]
    new_file: bool
    ignore_cache: bool
    save_temp_on_complete: bool
    overwrite: bool
    verbose: int
    drop_original: bool


class Settings(SettingsProtocol):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Settings':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_option(self, option_name: str, value: Any) -> None:
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
    def service(self) -> Type[BaseTranslator]:
        return getattr(self, '_service').value

    @property
    def service_host(self) -> Optional[str]:
        return getattr(self, '_service_host', None)

    @property
    def processes(self) -> int:
        return getattr(self, '_processes', 1)

    @property
    def webdriver(self) -> Optional[Path]:
        return getattr(self, '_webdriver', None)

    @property
    def new_file(self) -> bool:
        return getattr(self, '_new_file', False)

    @property
    def ignore_cache(self) -> bool:
        return getattr(self, '_ignore_cache', False)

    @property
    def save_temp_on_complete(self) -> bool:
        return getattr(self, '_save_temp_on_complete', False)

    @property
    def overwrite(self) -> bool:
        return getattr(self, '_overwrite', False)

    @property
    def verbose(self) -> int:
        return getattr(self, '_verbose', 0)

    @property
    def drop_original(self) -> bool:
        return getattr(self, '_drop_original', False)
