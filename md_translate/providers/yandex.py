import urllib.parse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from md_translate.providers._base import Provider


class YandexTranslateProvider(Provider):
    HEADLESS = False

    def __init__(self):
        super().__init__()
        self._host = 'https://translate.yandex.com'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'lang': f'{from_language}-{to_language}',
        }
        url = f'{self._host}/?{urllib.parse.urlencode(params)}'
        self._driver.get(url)
        textarea = self._driver.find_element(by=By.CLASS_NAME, value='textinput')
        result_container = self._driver.find_element(by=By.ID, value='textbox2')
        textarea.send_keys(text)

        WebDriverWait(self._driver, 10).until(lambda driver: result_container.text != '')
        data = result_container.text
        data = data.replace('\n ', '  ')
        return data




