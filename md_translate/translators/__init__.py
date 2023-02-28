import enum

from ._base_translator import BaseTranslator  # NOQA
from .bing import BingTranslateProvider
from .deepl import DeeplTranslateProvider
from .google import GoogleTranslateProvider
from .yandex import YandexTranslateProvider


class Translator(enum.Enum):
    yandex = YandexTranslateProvider
    google = GoogleTranslateProvider
    bing = BingTranslateProvider
    deepl = DeeplTranslateProvider
