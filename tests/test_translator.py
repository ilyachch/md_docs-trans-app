import unittest
from unittest import mock

from requests.exceptions import ConnectionError
from requests import Response
from md_translate.translator import YandexTranslator, get_translator_by_name, GoogleTranslator, \
    AbstractTranslator


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


class TestTranslatorFails(unittest.TestCase):
    string_to_translate = 'Some string'

    class MockedSettingsYandex:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = 'Yandex'

    class MockedSettingsGoogle:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = 'Google'

    class MockedResponseEnRuFailed:
        ok = False

    @mock.patch('md_translate.translator.requests.post')
    def test_yandex_translation_requesting_fails(self, mocked_post):
        mocked_post.return_value = self.MockedResponseEnRuFailed
        with self.assertRaises(ConnectionError):
            YandexTranslator(self.MockedSettingsYandex()).request_translation(self.string_to_translate)

    @mock.patch('md_translate.translator.requests.post')
    def test_google_translation_requesting_fails(self, mocked_post):
        mocked_post.return_value = self.MockedResponseEnRuFailed
        with self.assertRaises(ConnectionError):
            GoogleTranslator(self.MockedSettingsYandex()).request_translation(self.string_to_translate)


class TestYandexTranslator(unittest.TestCase):
    en_string_to_translate = 'Some string to translate'
    en_translated_string = 'Переведенная строка'

    ru_string_to_translate = 'Переведенная строка'
    ru_translated_string = 'Some string to translate'

    @staticmethod
    def get_settings_class(source, target):
        class MockedSettings:
            api_key = 'TEST_API_KEY'
            service = 'Yandex'
            source_lang = source
            target_lang = target

        return MockedSettings

    @staticmethod
    def get_ok_response_mock(source):
        class MockedResponse:
            ok = True
            if source == 'en':
                translated_string = TestYandexTranslator.en_translated_string
            elif source == 'ru':
                translated_string = TestYandexTranslator.ru_translated_string

            def json(s):
                return {'text': [s.translated_string, ]}

        return MockedResponse

    def setUp(self):
        self.en_ru_settings = self.get_settings_class('en', 'ru')()
        self.ru_en_settings = self.get_settings_class('ru', 'en')()

        self.en_ru_response = self.get_ok_response_mock('en')()
        self.ru_en_response = self.get_ok_response_mock('ru')()

    @mock.patch('md_translate.translator.requests.post')
    def test_en_ru_translation_ok(self, request_mock):
        request_mock.return_value = self.en_ru_response
        translate_result = YandexTranslator(self.en_ru_settings).request_translation(self.en_string_to_translate)
        request_mock.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': self.en_string_to_translate}, params={'key': 'TEST_API_KEY', 'lang': 'en-ru'}
        )
        self.assertEqual(translate_result, self.en_translated_string)

    @mock.patch('md_translate.translator.requests.post')
    def ru_en_translation_ok(self, request_mock):
        request_mock.return_value = self.ru_en_response
        translate_result = YandexTranslator(self.ru_en_settings).request_translation(self.ru_string_to_translate)
        request_mock.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': self.ru_string_to_translate}, params={'key': 'TEST_API_KEY', 'lang': 'en-ru'}
        )
        self.assertEqual(translate_result, self.ru_translated_string)


class TestGoogleTranslator(unittest.TestCase):
    en_string_to_translate = 'Some string to translate'
    en_translated_string = 'Переведенная строка'

    ru_string_to_translate = 'Переведенная строка'
    ru_translated_string = 'Some string to translate'

    @staticmethod
    def get_settings_class(source, target):
        class MockedSettings:
            api_key = 'TEST_API_KEY'
            service = 'Google'
            source_lang = source
            target_lang = target

        return MockedSettings

    @staticmethod
    def get_ok_response_mock(source):
        class MockedResponse:
            ok = True
            if source == 'en':
                translated_string = TestGoogleTranslator.en_translated_string
            elif source == 'ru':
                translated_string = TestGoogleTranslator.ru_translated_string

            def json(s):
                return {'data': {'translations': [{'translatedText': s.translated_string}]}}

        return MockedResponse

    def setUp(self):
        self.en_ru_settings = self.get_settings_class('en', 'ru')()
        self.ru_en_settings = self.get_settings_class('ru', 'en')()

        self.en_ru_response = self.get_ok_response_mock('en')()
        self.ru_en_response = self.get_ok_response_mock('ru')()

    @mock.patch('md_translate.translator.requests.post')
    def test_en_ru_translation_ok(self, request_mock):
        request_mock.return_value = self.en_ru_response
        translate_result = GoogleTranslator(self.en_ru_settings).request_translation(self.en_string_to_translate)
        request_mock.assert_called_with(
            'https://translation.googleapis.com/language/translate/v2',
            headers={'Authorization': 'Bearer "TEST_API_KEY"'},
            data={'q': self.en_string_to_translate, 'source': 'en', 'target': 'ru', 'format': 'text'},
        )
        self.assertEqual(translate_result, self.en_translated_string)

    @mock.patch('md_translate.translator.requests.post')
    def ru_en_translation_ok(self, request_mock):
        request_mock.return_value = self.ru_en_response
        translate_result = GoogleTranslator(self.ru_en_settings).request_translation(self.ru_string_to_translate)
        request_mock.assert_called_with(
            'https://translation.googleapis.com/language/translate/v2',
            headers={'Authorization': 'Bearer "TEST_API_KEY"'},
            data={'q': self.en_string_to_translate, 'source': 'en', 'target': 'ru', 'format': 'text'},
        )
        self.assertEqual(translate_result, self.ru_translated_string)


class TestAbstractTranslatorFails(unittest.TestCase):
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'ru'
        target_lang = 'en'

    def test_abstract_method_usage_fails(self):
        abstract_translator_object = AbstractTranslator(self.MockedSettings())
        with self.assertRaises(NotImplementedError):
            abstract_translator_object.request_for_translation('some_string')
        with self.assertRaises(NotImplementedError):
            abstract_translator_object.process_response(Response())
