import abc
import pathlib
import urllib.parse
from typing import Dict, Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

current_dir = pathlib.Path(__file__).parent.absolute()


class TranslationProvider(abc.ABC):
    DEFAULT_DRIVER_NAME = 'chromedriver'

    HEADLESS = True

    WEBDRIVER_WAIT = WebDriverWait
    WEBDRIVER_BY = By

    HOST: Optional[str] = None

    def __init__(self, host: Optional[str] = None) -> None:
        self._session = requests.Session()
        self._selected_driver = self.DEFAULT_DRIVER_NAME
        self._host = host or self.HOST
        if self._host is None:
            raise ValueError('Host is not defined')

    def __enter__(self):
        options = Options()
        if self.HEADLESS:
            options.add_argument('--headless')
        self._driver = webdriver.Chrome(
            executable_path=str(current_dir / 'bin' / self._selected_driver), options=options
        )
        return self

    def __exit__(self, *args, **kwargs):
        self._driver.quit()

    @abc.abstractmethod
    def translate(self, from_language: str, to_language: str, text: str) -> str:
        raise NotImplementedError()

    def get_url(self, params: Dict[str, str]) -> str:
        return f'{self._host}?{urllib.parse.urlencode(params)}'

    def cookies_accept(self) -> None:
        cookies_accept_button = self._driver.find_element(
            by=self.WEBDRIVER_BY.XPATH, value='//*[text()="Accept all"]'
        )
        if cookies_accept_button:
            cookies_accept_button.click()

    @staticmethod
    def get_cleaned_data(data: str) -> str:
        paragraphs = data.split('\n')
        paragraphs = [paragraph.strip() for paragraph in paragraphs]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        return '\n'.join(paragraphs)
