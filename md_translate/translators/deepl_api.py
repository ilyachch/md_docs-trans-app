import requests

from ._api_base import APIBaseTranslator


class DeeplAPITranslateProvider(APIBaseTranslator):
    HOST = 'https://api-free.deepl.com/'

    API_KEY_SETTINGS_PARAM = 'deepl_api_key'

    def make_request(self, *, text: str) -> requests.Response:
        headers = {
            'Authorization': f'DeepL-Auth-Key {self.api_key}',
        }
        request_body = {
            'text': [
                text,
            ],
            'source_lang': self.from_language.upper(),
            'target_lang': self.to_language.upper(),
        }

        response = self._session.post(
            url=f'{self.HOST}v2/translate',
            headers=headers,
            json=request_body,
        )
        response.raise_for_status()
        return response

    def get_translated_data(self, response: requests.Response) -> str:
        return response.json()['translations'][0]['text']
