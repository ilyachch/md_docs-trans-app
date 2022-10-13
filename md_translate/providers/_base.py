import requests

import abc


class Provider(abc.ABC):
    def __init__(self):
        self._session = requests.Session()

    @abc.abstractmethod
    def translate(self, from_language: str, to_language: str, text: str) -> str:
        raise NotImplementedError()
