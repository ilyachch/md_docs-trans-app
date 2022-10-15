from md_translate.providers._base import TranslationProvider


class YandexTranslateProvider(TranslationProvider):
    HOST = 'https://translate.yandex.com/'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'lang': f'{from_language}-{to_language}',
        }
        self._driver.get(self.get_url(params))
        textarea = self._driver.find_element(by=self.WEBDRIVER_BY.CLASS_NAME, value='textinput')
        result_container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='textbox2')
        textarea.send_keys(text)

        self.WEBDRIVER_WAIT(self._driver, 10).until(lambda driver: result_container.text != '')
        data = result_container.text
        return self.get_cleaned_data(data)
