import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from settings import Settings


class BaseTranslator(metaclass=abc.ABCMeta):
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
