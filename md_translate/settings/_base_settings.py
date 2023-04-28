import enum
import json
from pathlib import Path
from typing import Any, Optional, Protocol, Type, Union

from translators import BaseTranslator


class SettingsProtocol(Protocol):
    path: Union[Path, list[Path]]
    from_lang: str
    to_lang: str
    service: Type[BaseTranslator]
    processes: int
    new_file: bool
    ignore_cache: bool
    save_temp_on_complete: bool
    overwrite: bool
    verbose: int
    drop_original: bool


class SettingsJsonEncoder(json.JSONEncoder):
    IGNORED_ATTRIBUTES = ['_instance']

    def default(self, o: Any) -> Any:
        if isinstance(o, enum.Enum):
            return o.name
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, Settings):
            return {
                key[1:]: value
                for key, value in o.__dict__.items()
                if key.startswith('_') and key not in self.IGNORED_ATTRIBUTES
            }
        return super().default(o)


class Settings(SettingsProtocol):
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Settings':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def update_from_config(self, file_path: Optional[Path]) -> None:
        if file_path is None:
            file_path = Path('$HOME/.config/md_translate/config.json').expanduser()
        if not file_path.exists():
            return
        file_data = json.loads(file_path.read_text())
        for option_name, value in file_data.items():
            self.set_option(option_name, value)

    def dump(self) -> None:
        print(json.dumps(self, indent=4, cls=SettingsJsonEncoder))

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
    def processes(self) -> int:
        return getattr(self, '_processes', 1)

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
