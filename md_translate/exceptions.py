from typing import Type

import click


class MdTranslateException(Exception):  # pragma: no cover
    pass


class NoMdFilesFound(MdTranslateException, click.ClickException):  # pragma: no cover
    pass


class NoCacheFileFound(MdTranslateException, click.ClickException):  # pragma: no cover
    pass


def safe_run(exception_to_catch: Type[Exception], default_return_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_to_catch:
                return default_return_value

        return wrapper

    return decorator
