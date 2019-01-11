import os
import unittest
from unittest import mock

from md_translate.translator import Translator


class TestTranslatorException(unittest.TestCase):
    def setUp(self):
        Translator.API_KEY = None

    def test_api_key_exception(self):
        with self.assertRaises(FileNotFoundError):
            Translator()


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.api_key = 'TEST_API_KEY'
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.api_key_path = os.path.join(dir_path, 'data', 'test_data', 'API_KEY')
        self.api_key_backup = Translator.api_key_filename
        Translator.api_key_filename = self.api_key_path

    def test_api_key_caching(self):
        translator1 = Translator()
        self.assertEqual(Translator.API_KEY, self.api_key)
        translator2 = Translator()
        self.assertNotEqual(translator1, translator2)
        self.assertEqual(translator1.api_key, translator2.api_key)

    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post):
        string_to_translate = 'Some string to translate'
        translated_string = 'Some string to translate'

        class ResponseMock:
            ok = True

            def json(self):
                return {'data': [translated_string, ]}

        mocked_post.return_value = ResponseMock()
        translate_result = Translator().request_translation(string_to_translate)
        mocked_post.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate?key=TEST_API_KEY&lang=en-ru',
            {'text': string_to_translate}
        )
        self.assertEqual(translate_result, translated_string)

    def tearDown(self):
        Translator.api_key_filename = self.api_key_backup
        Translator.API_KEY = None
