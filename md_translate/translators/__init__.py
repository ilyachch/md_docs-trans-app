import pathlib
from typing import Any, Dict, Optional, Protocol, Type, Union, runtime_checkable

from .bing import BingTranslateProvider
from .deepl import DeeplTranslateProvider
from .google import GoogleTranslateProvider
from .yandex import YandexTranslateProvider

TRANSLATION_SERVICE_YANDEX = 'yandex'
TRANSLATION_SERVICE_GOOGLE = 'google'
TRANSLATION_SERVICE_BING = 'bing'
TRANSLATION_SERVICE_DEEPL = 'deepl'


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


TRANSLATOR_BY_SERVICE_NAME: Dict[str, Type[PTranslator]] = {
    TRANSLATION_SERVICE_YANDEX: YandexTranslateProvider,
    TRANSLATION_SERVICE_GOOGLE: GoogleTranslateProvider,
    TRANSLATION_SERVICE_BING: BingTranslateProvider,
    TRANSLATION_SERVICE_DEEPL: DeeplTranslateProvider,
}
