import abc
from typing import TYPE_CHECKING, Any

import requests

from md_translate.translators import BaseTranslator

if TYPE_CHECKING:
    from md_translate.settings import Settings


class APIBaseTranslator(BaseTranslator):
    HOST: str

    API_KEY_SETTINGS_PARAM: str

    def __init__(self, settings: 'Settings') -> None:
        self._settings = settings
        self.from_language = settings.from_lang
        self.to_language = settings.to_lang
        self.api_key = getattr(settings, self.API_KEY_SETTINGS_PARAM)
        if not self.api_key:
            raise ValueError('API key is not set')

    def __enter__(self) -> 'BaseTranslator':
        self._session = requests.Session()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self._session.close()

    def translate(self, *, text: str) -> str:
        response = self.make_request(text=text)
        return self.get_translated_data(response)

    @abc.abstractmethod
    def make_request(self, *, text: str) -> requests.Response: ...

    @abc.abstractmethod
    def get_translated_data(self, response: requests.Response) -> str: ...
