from typing import TYPE_CHECKING, Any, Callable, Optional, Type, TypedDict, cast

import click
from click.decorators import _param_memo
from pydantic import Field

if TYPE_CHECKING:
    from ._base_settings import Settings


class ClickFieldInfoExtra(TypedDict):
    click_option_name: list[str]
    click_option_type: Any
    click_option_help: str
    click_option_required: bool
    click_option_callback: Optional[Callable]
    click_option_is_flag: bool
    click_option_default: Any
    click_option_count: bool


def SettingsToCliField(  # noqa: N802
    *args: Any,
    click_option_name: list[str],
    click_option_type: Optional[click.ParamType] = None,
    click_option_help: str = '',
    click_option_required: bool = False,
    click_option_callback: Optional[Callable] = None,
    click_option_is_flag: bool = False,
    click_option_default: Any = None,
    click_option_count: bool = False,
    **kwargs: Any,
) -> Any:
    return Field(
        *args,
        **kwargs,
        click_option_name=click_option_name,
        click_option_type=click_option_type,
        click_option_required=click_option_required,
        click_option_help=click_option_help,
        click_option_callback=click_option_callback,
        click_option_is_flag=click_option_is_flag,
        click_option_default=click_option_default,
        click_option_count=click_option_count,
    )


def build_cli_options_from_settings(settings: Type['Settings']) -> list[click.Option]:
    options = []
    for option_name, option in settings.__fields__.items():
        click_option_info = cast(ClickFieldInfoExtra, option.field_info.extra)
        if option_name.startswith('_') or not click_option_info:
            continue  # pragma: no cover
        options.append(
            click.Option(
                click_option_info['click_option_name'],
                type=click_option_info['click_option_type'],
                required=cast(bool, click_option_info['click_option_required']),
                help=cast(str, click_option_info['click_option_help']),
                callback=cast(Callable, click_option_info['click_option_callback']),
                is_flag=cast(bool, click_option_info['click_option_is_flag']),
                default=click_option_info['click_option_default'],
                count=cast(bool, click_option_info['click_option_count']),
            )
        )
    return options


def wrap_command_with_options(
    settings: Type['Settings'],
) -> Callable:
    def decorator(func: Callable) -> Callable:
        for option in reversed(build_cli_options_from_settings(settings)):
            _param_memo(func, option)
        return func

    return decorator
