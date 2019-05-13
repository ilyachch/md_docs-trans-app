import unittest
from unittest import mock

from md_translate.translator import YandexTranslator, get_translator_by_name, GoogleTranslator


class TestGetTranslator(unittest.TestCase):
    def test_get_translator_yandex(self):
        service = 'Yandex'
        service_parser = get_translator_by_name(service)
        self.assertEqual(service_parser, YandexTranslator)
        self.assertNotEqual(service_parser, GoogleTranslator)

    def test_get_translator_google(self):
        service = 'Google'
        service_parser = get_translator_by_name(service)
        self.assertEqual(service_parser, GoogleTranslator)
        self.assertNotEqual(service_parser, YandexTranslator)


class TestTranslatorYandexEnRu(unittest.TestCase):
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = 'Yandex'

    class MockedResponseEnRu:
        translated_string = 'Переведенная строка'
        ok = True

        def json(self):
            return {'text': [self.translated_string, ]}

    def setUp(self):
        self.string_to_translate = 'Some string to translate'
        self.translated_string = 'Переведенная строка'

        self.mocked_settings = self.MockedSettings()
        self.mocked_response = self.MockedResponseEnRu()

    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post):
        mocked_post.return_value = self.mocked_response
        translate_result = YandexTranslator(self.mocked_settings).request_translation(self.string_to_translate)
        mocked_post.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': self.string_to_translate}, params={'key': 'TEST_API_KEY', 'lang': 'en-ru'}
        )
        self.assertEqual(translate_result, self.translated_string)


class TestTranslatorYandexRuEn(unittest.TestCase):
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'ru'
        target_lang = 'en'
        service = 'Yandex'

    class MockedResponseRuEn:
        translated_string = 'Some string to translate'
        ok = True

        def json(self):
            return {'text': [self.translated_string, ]}

    def setUp(self):
        self.string_to_translate = 'Переведенная строка'
        self.translated_string = 'Some string to translate'

        self.mocked_settings = self.MockedSettings()
        self.mocked_response = self.MockedResponseRuEn()

    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post):
        mocked_post.return_value = self.mocked_response
        translate_result = YandexTranslator(self.mocked_settings).request_translation(self.string_to_translate)
        mocked_post.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': self.string_to_translate}, params={'key': 'TEST_API_KEY', 'lang': 'ru-en'}
        )
        self.assertEqual(translate_result, self.translated_string)


class TestTranslatorGoogleEnRu(unittest.TestCase):
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = 'Google'

    class MockedResponseEnRu:
        translated_string = 'Переведенная строка'
        ok = True

        def json(self):
            return {'data': {'translations': [{'translatedText': self.translated_string}]}}

    def setUp(self):
        self.string_to_translate = 'Some string to translate'
        self.translated_string = 'Переведенная строка'

        self.mocked_settings = self.MockedSettings()
        self.mocked_response = self.MockedResponseEnRu()

    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post):
        mocked_post.return_value = self.mocked_response
        translate_result = GoogleTranslator(self.mocked_settings).request_translation(self.string_to_translate)
        mocked_post.assert_called_with(
            'https://translation.googleapis.com/language/translate/v2',
            headers={'Authorization': 'Bearer "TEST_API_KEY"'},
            data={'q': 'Some string to translate', 'source': 'en', 'target': 'ru', 'format': 'text'},
        )
        self.assertEqual(translate_result, self.translated_string)


class TestTranslatorGoogleRuEn(unittest.TestCase):
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'ru'
        target_lang = 'en'
        service = 'Google'

    class MockedResponseRuEn:
        translated_string = 'Some string to translate'
        ok = True

        def json(self):
            return {'data': {'translations': [{'translatedText': self.translated_string}]}}

    def setUp(self):
        self.string_to_translate = 'Переведенная строка'
        self.translated_string = 'Some string to translate'

        self.mocked_settings = self.MockedSettings()
        self.mocked_response = self.MockedResponseRuEn()

    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post):
        mocked_post.return_value = self.mocked_response
        translate_result = GoogleTranslator(self.mocked_settings).request_translation(self.string_to_translate)
        mocked_post.assert_called_with(
            'https://translation.googleapis.com/language/translate/v2',
            headers={'Authorization': 'Bearer "TEST_API_KEY"'},
            data={'q': 'Переведенная строка', 'source': 'ru', 'target': 'en', 'format': 'text'},
        )
        self.assertEqual(translate_result, self.translated_string)
