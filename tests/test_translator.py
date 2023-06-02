import pytest

from md_translate.translators import (
    BingTranslateProvider,
    DeeplTranslateProvider,
    GoogleTranslateProvider,
    YandexTranslateProvider,
)


@pytest.mark.skip(reason='Only for manual testing')
class TestTranslator:
    @pytest.mark.parametrize(
        'translator, source_text, expected',
        [
            (YandexTranslateProvider, 'Hello world', 'Привет, мир'),
            (GoogleTranslateProvider, 'Hello world', 'Привет, мир'),
            (BingTranslateProvider, 'Hello world', 'Всем привет'),
            (DeeplTranslateProvider, 'Hello world', 'Здравствуй мир'),
        ],
    )
    def test_translate(self, translator, source_text, expected):
        translator = translator(from_language='en', to_language='ru')
        with translator as translator_:
            assert translator_.translate(text=source_text) == expected
