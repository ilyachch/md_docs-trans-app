import pytest

from md_translate import const
from md_translate.exceptions import UnknownServiceError
from md_translate.utils import get_translator_by_service_name


class TestUtils:
    @pytest.mark.parametrize('service_name, translator', [
        [const.TRANSLATION_SERVICE_YANDEX, const.yandex],
        [const.TRANSLATION_SERVICE_GOOGLE, const.google],
        [const.TRANSLATION_SERVICE_BING, const.bing],
        [const.TRANSLATION_SERVICE_DEEPL, const.deepl],
        ['bad service name', None],
    ])
    def test_get_translator_class(self, service_name, translator):
        if service_name in const.TRANSLATOR_BY_SERVICE_NAME:
            assert get_translator_by_service_name(service_name) == translator
        else:
            with pytest.raises(UnknownServiceError):
                get_translator_by_service_name(service_name)
