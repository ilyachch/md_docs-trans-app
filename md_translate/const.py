from md_translate.translator import GoogleTranslator, YandexTranslator

TRANSLATION_SERVICE_YANDEX = 'Yandex'
TRANSLATION_SERVICE_GOOGLE = 'Google'

TRANSLATOR_BY_SERVICE_NAME = {
    TRANSLATION_SERVICE_YANDEX: YandexTranslator,
    TRANSLATION_SERVICE_GOOGLE: GoogleTranslator,
}

LANG_RU = 'ru'
LANG_EN = 'en'

AVAILABLE_LANGS = [LANG_EN, LANG_RU]
