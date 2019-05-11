from typing import Type

import requests

from md_translate.arguments_processor import settings


class Translator:
    BASE_API_URL = None

    def request_translation(self, string_to_translate: str):
        response = self.request_for_translation(string_to_translate)
        if response.ok:
            translated_data = self.process_response(response)
            return '\n'.join(translated_data)
        else:
            raise requests.exceptions.ConnectionError('Something web wrong with translation requesting.')

    def request_for_translation(self, string_to_translate: str):
        raise NotImplementedError()

    def process_response(self, response: requests.Response):
        raise NotImplementedError()


def get_translator_by_name(name) -> Type[Translator]:
    if name == 'Yandex':
        return YandexTranslator
    elif name == 'Google':
        return GoogleTranslator


class YandexTranslator(Translator):
    BASE_API_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    def request_for_translation(self, string_to_translate):
        params = {'key': settings.api_key,
                  'lang': '-'.join([settings.source_lang, settings.target_lang]),
                  }
        data = {'text': string_to_translate}
        return requests.post(self.BASE_API_URL, params=params,
                             data=data
                             )

    def process_response(self, response):
        return response.json()['text']


class GoogleTranslator(Translator):
    BASE_API_URL = 'https://translation.googleapis.com/language/translate/v2'

    def request_for_translation(self, string_to_translate):
        headers = {'Authorization': 'Bearer "{}"'.format(settings.api_key)}
        data = {'q': string_to_translate,
                'source': settings.source_lang,
                'target': settings.target_lang,
                'format': 'text'}
        return requests.post(self.BASE_API_URL, headers=headers, data=data)

    def process_response(self, response):
        return response.json()['data']['translations'][0]['translatedText']
