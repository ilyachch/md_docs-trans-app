import abc
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from settings import SettingsProtocol


class BaseTranslatorProtocol(Protocol):
    def translate(self, *, text: str) -> str:
        ...


class BaseTranslator(BaseTranslatorProtocol, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, settings: 'SettingsProtocol') -> None:
        ...

    @abc.abstractmethod
    def __enter__(self) -> 'BaseTranslator':
        ...

    @abc.abstractmethod
    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        ...

    @abc.abstractmethod
    def translate(self, *, text: str) -> str:
        ...
