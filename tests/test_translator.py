import unittest
from unittest import mock

from requests.exceptions import ConnectionError

from md_translate.translator import YandexTranslator, GoogleTranslator

EN_STR = 'Some string to translate'
RU_STR = 'Переведенная строка'


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
        from md_translate import settings
        settings.settings = self.MockedSettingsYandex()
        mocked_post.return_value = self.MockedResponseEnRuFailed
        with self.assertRaises(ConnectionError):
            YandexTranslator().request_translation(self.string_to_translate)

    @mock.patch('md_translate.translator.requests.post')
    def test_google_translation_requesting_fails(self, mocked_post):
        from md_translate import settings
        settings.settings = self.MockedSettingsGoogle()
        mocked_post.return_value = self.MockedResponseEnRuFailed
        with self.assertRaises(ConnectionError):
            GoogleTranslator().request_translation(self.string_to_translate)


class TestYandexTranslator(unittest.TestCase):
    en_string_to_translate = EN_STR
    en_translated_string = RU_STR

    ru_string_to_translate = RU_STR
    ru_translated_string = EN_STR

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
        from md_translate import settings
        settings.settings = self.en_ru_settings
        request_mock.return_value = self.en_ru_response
        translate_result = YandexTranslator().request_translation(self.en_string_to_translate)
        request_mock.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': self.en_string_to_translate}, params={'key': 'TEST_API_KEY', 'lang': 'en-ru'}
        )
        self.assertEqual(translate_result, self.en_translated_string)

    @mock.patch('md_translate.translator.requests.post')
    def ru_en_translation_ok(self, request_mock):
        from md_translate import settings
        settings.settings = self.ru_en_settings
        request_mock.return_value = self.ru_en_response
        translate_result = YandexTranslator().request_translation(self.ru_string_to_translate)
        request_mock.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': self.ru_string_to_translate}, params={'key': 'TEST_API_KEY', 'lang': 'en-ru'}
        )
        self.assertEqual(translate_result, self.ru_translated_string)


class TestGoogleTranslator(unittest.TestCase):
    en_string_to_translate = EN_STR
    en_translated_string = RU_STR

    ru_string_to_translate = RU_STR
    ru_translated_string = EN_STR

    @staticmethod
    def get_settings_class(source, target):
        class MockedSettings:
            api_key = 'TEST_API_KEY'
            service_name = 'Google'
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
        from md_translate import settings
        settings.settings = self.en_ru_settings
        request_mock.return_value = self.en_ru_response
        translate_result = GoogleTranslator().request_translation(self.en_string_to_translate)
        request_mock.assert_called_with(
            'https://translation.googleapis.com/language/translate/v2',
            headers={'Authorization': 'Bearer "TEST_API_KEY"'},
            data={'q': self.en_string_to_translate, 'source': 'en', 'target': 'ru', 'format': 'text'},
        )
        self.assertEqual(translate_result, self.en_translated_string)

    @mock.patch('md_translate.translator.requests.post')
    def ru_en_translation_ok(self, request_mock):
        from md_translate import settings
        settings.settings = self.ru_en_settings
        request_mock.return_value = self.ru_en_response
        translate_result = GoogleTranslator().request_translation(self.ru_string_to_translate)
        request_mock.assert_called_with(
            'https://translation.googleapis.com/language/translate/v2',
            headers={'Authorization': 'Bearer "TEST_API_KEY"'},
            data={'q': self.en_string_to_translate, 'source': 'en', 'target': 'ru', 'format': 'text'},
        )
        self.assertEqual(translate_result, self.ru_translated_string)
