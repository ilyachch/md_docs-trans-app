import unittest
from unittest import mock

from md_translate.translator import YandexTranslator




class TestTranslator(unittest.TestCase):
    class MockedSettings:
        api_key = 'TEST_API_KEY'
        source_lang = 'en'
        target_lang = 'ru'
        service = 'Yandex'

    class MockedResponse:
        translated_string = 'Переведенная строка'
        ok = True

        def json(self):
            return {'text': [self.translated_string, ]}

    def setUp(self):
        self.string_to_translate = 'Some string to translate'
        self.translated_string = 'Переведенная строка'

        self.mocked_settings = self.MockedSettings()
        self.mocked_response = self.MockedResponse()

    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post):
        mocked_post.return_value = self.mocked_response
        translate_result = YandexTranslator(self.mocked_settings).request_translation(self.string_to_translate)
        mocked_post.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            data={'text': 'Some string to translate'}, params={'key': 'TEST_API_KEY', 'lang': 'en-ru'}
        )
        self.assertEqual(translate_result, self.translated_string)
