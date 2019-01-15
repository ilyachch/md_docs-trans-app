import unittest
from unittest import mock

from md_translate.translator import Translator


# TODO: move to integration test
# class TestTranslatorException(unittest.TestCase):
#     def setUp(self):
#         dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#         empty_path = os.path.join(dir_path, 'data', 'TRANSLATE_API_KEY')
#         self.backup_api_path =
#         Translator.api_key_filename = empty_path
#         Translator.API_KEY = None
#
#     def test_api_key_exception(self):
#         with self.assertRaises(FileNotFoundError):
#             Translator()
#
#     def tearDown(self):
#         Translator.API_KEY = None


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.string_to_translate = 'Some string to translate'
        self.translated_string = 'Переведенная строка'

        class MockedSettings:
            api_key = 'TEST_API_KEY'
            lang_string = 'en-ru'

        class MockedResponse:
            ok = True

            def json(s):
                return {'text': [self.translated_string, ]}

        self.mocked_settings = MockedSettings()
        self.mocked_response = MockedResponse()

    @mock.patch('md_translate.translator.Settings')
    @mock.patch('md_translate.translator.requests.post')
    def test_translation_requesting(self, mocked_post, mocked_settings):
        mocked_settings.return_value = self.mocked_settings
        mocked_post.return_value = self.mocked_response
        translate_result = Translator().request_translation(self.string_to_translate)
        mocked_post.assert_called_with(
            'https://translate.yandex.net/api/v1.5/tr.json/translate?key=TEST_API_KEY&lang=en-ru',
            {'text': self.string_to_translate}
        )
        self.assertEqual(translate_result, self.translated_string)
