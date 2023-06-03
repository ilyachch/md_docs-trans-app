import abc
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from md_translate.settings import Settings


class BaseTranslatorProtocol(Protocol):  # pragma: no cover
    def translate(self, *, text: str) -> str:
        ...


class BaseTranslator(BaseTranslatorProtocol, metaclass=abc.ABCMeta):  # pragma: no cover
    @abc.abstractmethod
    def __init__(self, settings: 'Settings') -> None:
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
