from typing import Type

from md_translate import const
from md_translate.exceptions import UnknownServiceError
from md_translate.translator import AbstractTranslator


def get_translator_class_by_service_name(service_name: str) -> Type[AbstractTranslator]:
    translator_class = const.TRANSLATOR_BY_SERVICE_NAME.get(service_name)
    if translator_class is None:
        raise UnknownServiceError(service_name)
    return translator_class
