import abc
import pathlib
from typing import Optional

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

current_dir = pathlib.Path(__file__).parent.absolute()


class Provider(abc.ABC):
    DEFAULT_DRIVER_NAME = 'chromedriver'

    HEADLESS = True

    WEBDRIVER_WAIT = WebDriverWait
    WEBDRIVER_BY = By

    def __init__(self):
        self._session = requests.Session()
        self._selected_driver = self.DEFAULT_DRIVER_NAME

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
