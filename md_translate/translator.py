import requests

from md_translate.arguments_processor import settings


def get_translator_by_name(name):
    if name == 'Yandex':
        return YandexTranslator
    elif name == 'Google':
        return GoogleTranslator


class Translator:
    BASE_API_URL = None

    def request_translation(self, string_to_translate):
        response = self.request_for_translation(string_to_translate)
        if response.ok:
            translated_data = self.process_response(response)
            return '\n'.join(translated_data)
        else:
            raise requests.exceptions.ConnectionError('Something web wrong with translation requesting.')

    def request_for_translation(self, string_to_translate):
        raise NotImplementedError()

    def process_response(self, response):
        raise NotImplementedError()


class YandexTranslator(Translator):
    BASE_API_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    def request_for_translation(self, string_to_translate):
        params = {'key': settings.api_key_value,
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
        headers = {'Authorization': 'Bearer "{}"'.format(settings.api_key_value)}
        data = {'q': string_to_translate,
                'source': settings.source_lang,
                'target': settings.target_lang,
                'format': 'text'}
        return requests.post(self.BASE_API_URL, headers=headers, data=data)

    def process_response(self, response):
        return response.json()['data']['translations'][0]['translatedText']
