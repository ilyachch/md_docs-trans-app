from pathlib import Path


class MdTranslateBaseException(Exception):
    pass


class ConfigurationError(MdTranslateBaseException):
    def __init__(self) -> None:
        super().__init__('Some of settings missed. Check your config file')


class ObjectNotFoundException(MdTranslateBaseException):
    def __init__(self, obj: Path) -> None:
        super().__init__(f'{obj} not found')


class NoApiKeyFileError(MdTranslateBaseException):
    def __init__(self, api_key_path: Path) -> None:
        super().__init__(
            f'API_KEY file in location "{api_key_path}" not found\n'
            'Provide API_KEY file path or create it, if not exist'
        )


class NoConfigFileError(MdTranslateBaseException):
    def __init__(self, not_found_file: Path) -> None:
        super().__init__(
            f'No config file found. Create file {not_found_file} or pass custom file  with `-c` param'
        )


class FileIsNotMarkdown(MdTranslateBaseException):
    def __init__(self, not_md_obj: Path) -> None:
        super().__init__(f'{not_md_obj} is not a Markdown file!')
