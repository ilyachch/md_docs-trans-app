from unittest import TestCase

from md_translate import const
from md_translate.exceptions import UnknownServiceError
from md_translate.translator import GoogleTranslator, YandexTranslator
from md_translate.utils import get_translator_class_by_service_name


class TestUtils(TestCase):
    def test_get_translator_class(self):
        self.assertEqual(get_translator_class_by_service_name(const.TRANSLATION_SERVICE_GOOGLE), GoogleTranslator)
        self.assertEqual(get_translator_class_by_service_name(const.TRANSLATION_SERVICE_YANDEX), YandexTranslator)

    def test_error_rising(self):
        with self.assertRaises(UnknownServiceError):
            get_translator_class_by_service_name('bad service name')
