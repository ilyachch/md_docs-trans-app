import pytest

from md_translate.translators import (
    BingTranslateProvider,
    DeeplTranslateProvider,
    GoogleTranslateProvider,
    YandexTranslateProvider,
    LibreTranslateTranslateProvider,
)


class MockSettings:
    from_lang = 'en'
    to_lang = 'ru'


@pytest.mark.web  # run it with `pytest -m web`
class TestTranslator:
    @pytest.mark.parametrize(
        'translator, source_text, expected',
        [
            (YandexTranslateProvider, 'Hello world', 'Привет, мир'),
            (GoogleTranslateProvider, 'Hello world', 'Привет, мир'),
            (BingTranslateProvider, 'Hello world', 'Всем привет'),
            (DeeplTranslateProvider, 'Hello world', 'Здравствуй мир'),
            (LibreTranslateTranslateProvider, 'Hello world', 'Привет мир'),
        ],
    )
    def test_translate(self, translator, source_text, expected):
        translator = translator(MockSettings())  # type: ignore
        with translator as translator_:
            assert translator_.translate(text=source_text) == expected
