from urllib.parse import urlencode

import requests

from settings import Settings


class Translator:
    base_api_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    def __init__(self):
        self.__settings = Settings()
        self.qqq = Settings()
        self.__request_url = self.__get_request_url()

    def __get_request_url(self):
        query_string = urlencode({
            'key': self.__settings.api_key,
            'lang': self.__settings.lang_string,
        })
        return '?'.join([self.base_api_url, query_string])

    def request_translation(self, string_to_translate):
        response = requests.post(self.__request_url, {'text': string_to_translate})
        if response.ok:
            response_data = response.json()
            translated_data = response_data['text']
            return '\n'.join(translated_data)
        else:
            raise requests.exceptions.ConnectionError('Something web wrong with translation requesting.')
