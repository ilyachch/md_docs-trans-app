import enum

from ._base_translator import BaseTranslator, BaseTranslatorProtocol  # noqa: F401
from .bing import BingTranslateProvider
from .deepl import DeeplTranslateProvider
from .deepl_api import DeeplAPITranslateProvider
from .google import GoogleTranslateProvider
from .libretranslate import LibreTranslateTranslateProvider
from .yandex import YandexTranslateProvider


class Translator(enum.Enum):
    yandex = YandexTranslateProvider
    google = GoogleTranslateProvider
    bing = BingTranslateProvider
    deepl = DeeplTranslateProvider
    libretranslate = LibreTranslateTranslateProvider
    deepl_api = DeeplAPITranslateProvider
