import abc


class Provider(abc.ABC):
    @abc.abstractmethod
    def translate(self, from_language: str, to_language: str, text: str) -> str:
        raise NotImplementedError()
