from pathlib import Path


class MdTranslateBaseException(Exception):
    pass


class UnknownServiceError(MdTranslateBaseException):
    def __init__(self, service_name: str) -> None:
        super().__init__(f'{service_name} service is unknown')


class ConfigurationError(MdTranslateBaseException):
    def __init__(self, property_name: str) -> None:
        super().__init__(
            f'The setting "{property_name}" is missing. Check your config file or cli arguments'
        )


class ObjectNotFoundException(MdTranslateBaseException):
    def __init__(self, obj: Path) -> None:
        super().__init__(f'{obj} not found')


class FileIsNotMarkdown(MdTranslateBaseException):
    def __init__(self, not_md_obj: Path) -> None:
        super().__init__(f'{not_md_obj} is not a Markdown file!')
