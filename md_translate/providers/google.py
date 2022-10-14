import pathlib
import urllib.parse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from ._base import Provider

current_dir = pathlib.Path(__file__).parent.absolute()


class GoogleTranslateProvider(Provider):
    def __init__(self):
        super().__init__()
        self._host = 'https://translate.google.com'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'sl': from_language,
            'tl': to_language,
        }
        url = f'{self._host}/?{urllib.parse.urlencode(params)}'
        self._driver.get(url)
        cookies_accept_button = self._driver.find_element(
            by=By.XPATH, value='//*[text()="Accept all"]'
        )
        if cookies_accept_button:
            cookies_accept_button.click()
        textarea = self._driver.find_element(by=By.TAG_NAME, value='textarea')
        result_container = self._driver.find_element(
            by=By.XPATH, value='//div[@aria-live="polite"]'
        )
        textarea.send_keys(text)
        WebDriverWait(self._driver, 10).until(lambda driver: result_container.text != '')
        result_element = result_container.find_element(
            by=By.CSS_SELECTOR, value=f'span[lang="{to_language}"]'
        )
        data = result_element.text
        data = data.replace('\n ', '  ')
        return data
