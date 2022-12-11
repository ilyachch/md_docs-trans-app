import enum
import pathlib
from typing import Any, Optional, Protocol, Union, runtime_checkable

from .bing import BingTranslateProvider
from .deepl import DeeplTranslateProvider
from .google import GoogleTranslateProvider
from .yandex import YandexTranslateProvider


@runtime_checkable
class PTranslator(Protocol):
    def __init__(
        self,
        from_language: str,
        to_language: str,
        webdriver_path: Optional[Union[str, pathlib.Path]] = None,
        host: Optional[str] = None,
    ) -> None:
        ...

    def translate(self, *, text: str) -> str:
        ...

    def __enter__(self) -> 'PTranslator':
        ...

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        ...


class Translator(enum.Enum):
    yandex = YandexTranslateProvider
    google = GoogleTranslateProvider
    bing = BingTranslateProvider
    deepl = DeeplTranslateProvider
