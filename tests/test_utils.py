from unittest import TestCase

from md_translate import const
from md_translate.exceptions import UnknownServiceError
from md_translate.utils import get_translator_by_service_name


class TestUtils(TestCase):
    def test_get_translator_class(self):
        self.assertEqual(get_translator_by_service_name(const.TRANSLATION_SERVICE_GOOGLE), const.google)
        self.assertEqual(get_translator_by_service_name(const.TRANSLATION_SERVICE_YANDEX), const.yandex)

    def test_error_rising(self):
        with self.assertRaises(UnknownServiceError):
            get_translator_by_service_name('bad service name')
