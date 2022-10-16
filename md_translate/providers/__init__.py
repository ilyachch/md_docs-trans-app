from .bing import BingTranslateProvider
from .deepl import DeeplTranslateProvider
from .google import GoogleTranslateProvider
from .yandex import YandexTranslateProvider

TRANSLATION_SERVICE_YANDEX = 'Yandex'
TRANSLATION_SERVICE_GOOGLE = 'Google'
TRANSLATION_SERVICE_BING = 'Bing'
TRANSLATION_SERVICE_DEEPL = 'Deepl'

TRANSLATOR_BY_SERVICE_NAME = {
    TRANSLATION_SERVICE_YANDEX: YandexTranslateProvider,
    TRANSLATION_SERVICE_GOOGLE: GoogleTranslateProvider,
    TRANSLATION_SERVICE_BING: BingTranslateProvider,
    TRANSLATION_SERVICE_DEEPL: DeeplTranslateProvider,
}
