import os
from urllib.parse import urlencode

import requests


class Translator:
    base_api_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    api_key_filename = 'TRANSLATE_API_KEY'

    source_lang = 'en'
    target_lang = 'ru'

    API_KEY = None

    def __init__(self):
        self.api_key = None
        self.__set_api_key()
        self.request_url = self.__get_request_url()

    def __get_request_url(self):
        lang_param = '{source}-{target}'.format(source=self.source_lang, target=self.target_lang)
        query_string = urlencode({
            'key': self.api_key,
            'lang': lang_param,
        })
        return '?'.join([self.base_api_url, query_string])

    def request_translation(self, string_to_translate):
        response = requests.post(self.request_url, {'text': string_to_translate})
        if response.ok:
            response_data = response.json()
            translated_data = response_data['text']
            return '\n'.join(translated_data)
        else:
            raise requests.exceptions.ConnectionError('Something web wrong with translation requesting.')

    def __set_api_key(self):
        if self.API_KEY is not None:
            self.api_key = self.API_KEY
        elif os.path.exists(self.api_key_filename):
            with open(self.api_key_filename) as api_key_file:
                api_key = api_key_file.read()
                Translator.API_KEY = api_key
                self.api_key = api_key
        else:
            raise FileNotFoundError('There is not found file "{filename}"!\n'
                                    'Please, create file with this name and \n'
                                    'put there your API key as plain text \n'
                                    'and restart application'.format(filename=self.api_key_filename))
