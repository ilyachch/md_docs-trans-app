import pathlib
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from ._base import Provider

current_dir = pathlib.Path(__file__).parent.absolute()


class GoogleTranslateProvider(Provider):
    def __init__(self):
        super().__init__()
        self._host = 'https://translate.google.com'

    def __enter__(self):
        options = Options()
        options.add_argument('--headless')
        self._driver = webdriver.Chrome(
            executable_path=current_dir / 'bin' / 'chromedriver', options=options
        )
        return self

    def __exit__(self, *args, **kwargs):
        self._driver.quit()

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'sl': from_language,
            'tl': to_language,
        }
        url = f'{self._host}/?{urllib.parse.urlencode(params)}'
        self._driver.get(url)
        self._driver.find_element(by=By.XPATH, value='//*[text()="Accept all"]').click()
        textarea = self._driver.find_element(by=By.TAG_NAME, value='textarea')
        # <div aria-live="polite" class="usGWQd" jsaction="copy:zVnXqd,r8sht;" jsname="r5xl4"></div>
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
