from typing import Any, Callable, Type

import click


class MdTranslateException(click.ClickException):  # pragma: no cover
    pass


class NoMdFilesFound(
    FileNotFoundError,
    click.ClickException,
):  # pragma: no cover
    pass


class NoTargetFileFound(
    FileNotFoundError,
    MdTranslateException,
):  # pragma: no cover
    pass


class NoCacheFileFound(
    FileNotFoundError,
    MdTranslateException,
):  # pragma: no cover
    pass


DecoratedFunction = Callable[..., Any]


def safe_run(exception_to_catch: Type[Exception], default_return_value: Any = None) -> Callable:
    def decorator(func: DecoratedFunction) -> DecoratedFunction:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exception_to_catch:
                return default_return_value

        return wrapper

    return decorator
