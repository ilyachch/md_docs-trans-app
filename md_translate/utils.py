from translators import apis  # type: ignore

from md_translate import const
from md_translate.exceptions import UnknownServiceError


def get_translator_by_service_name(service_name: str) -> apis.Tse:
    translator_class = const.TRANSLATOR_BY_SERVICE_NAME.get(service_name)
    if translator_class is None:
        raise UnknownServiceError(service_name)
    return translator_class
