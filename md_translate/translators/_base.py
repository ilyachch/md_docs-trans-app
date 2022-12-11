import abc
import logging
import pathlib
import time
import urllib.parse
from typing import Any, Optional, Union

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from md_translate.translators.randomizer.randomizer import Randomizer

current_dir = pathlib.Path(__file__).parent.absolute()
logger = logging.getLogger(__name__)


class AntiSpamException(Exception):
    pass


class TranslationProvider(metaclass=abc.ABCMeta):
    HEADLESS = False

    WEBDRIVER_WAIT = WebDriverWait
    WEBDRIVER_BY = By

    HOST: Optional[str] = None

    COOKIES_ACCEPT_BTN_TEXT = 'Accept all'

    ANTISPAM_TIMEOUT = 60 * 60  # 1 hour

    def __init__(
        self,
        from_language: str,
        to_language: str,
        webdriver_path: Optional[Union[str, pathlib.Path]] = None,
        host: Optional[str] = None,
    ) -> None:
        self._session = requests.Session()
        self._webdriver_path = webdriver_path
        self._host = self.__get_host(host)
        self.from_language = from_language
        self.to_language = to_language
        self.randomizer = Randomizer()

    def __get_host(self, host: Optional[str] = None) -> str:
        host = host or self.HOST
        if host is None:
            raise ValueError('Host is not defined')
        return host

    def __enter__(self) -> 'TranslationProvider':
        options = self.randomizer.make_options()
        if self._webdriver_path:
            self._driver = webdriver.Chrome(
                executable_path=str(self._webdriver_path), options=options
            )
        else:
            self._driver = webdriver.Chrome(options=options)

        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self._driver.quit()

    def translate(self, *, text: str) -> str:
        time.sleep(self.randomizer.get_random_sleep_time())
        self.load_page()
        if self.check_for_antispam():
            self.wait_for_antispam()
        input_element = self.get_input_element()
        input_element.send_keys(text)
        try:
            self.wait_for_translation()
        except AntiSpamException:
            self.wait_for_antispam()
            self.wait_for_translation()
        output_element = self.get_output_element()
        if self.check_for_antispam():
            self.wait_for_antispam()

        data = self.get_translated_data(output_element)
        clean_data = self.clear(data)
        return clean_data

    def load_page(self) -> None:
        url = self.get_url()
        self._driver.get(url)
        self.wait_for_page_load()
        self.accept_cookies()
        self.wait_for_page_load()

    @abc.abstractmethod
    def get_url(self) -> str:
        ...

    @abc.abstractmethod
    def check_for_antispam(self) -> bool:
        ...

    @abc.abstractmethod
    def accept_cookies(self) -> None:
        ...

    @abc.abstractmethod
    def get_input_element(self) -> WebElement:
        ...

    @abc.abstractmethod
    def get_output_element(self) -> WebElement:
        ...

    @staticmethod
    def get_translated_data(output_element: WebElement) -> str:
        return output_element.text

    @abc.abstractmethod
    def check_for_translation(self) -> bool:
        ...

    def wait_for_page_load(self) -> None:
        def wait_for(driver: Any) -> bool:
            return driver.execute_script('return document.readyState') == 'complete'

        self.WEBDRIVER_WAIT(self._driver, 10).until(wait_for)

    def click_cookies_accept(self, btn_text: str) -> None:
        try:
            cookies_accept_button = self._driver.find_element(
                by=self.WEBDRIVER_BY.XPATH, value=f'//*[text()="{btn_text}"]'
            )
            if cookies_accept_button:
                cookies_accept_button.click()
        except NoSuchElementException:
            return

    def wait_for_antispam(self) -> None:
        logger.debug('Waiting for antispam')
        self._driver.switch_to.window(self._driver.window_handles[0])

        def wait_for(driver: Any) -> bool:
            return not self.check_for_antispam()

        if self.check_for_antispam():
            self.WEBDRIVER_WAIT(self._driver, self.ANTISPAM_TIMEOUT).until(wait_for)

    def wait_for_translation(self) -> None:
        def wait_for(driver: Any) -> bool:
            if self.check_for_antispam():
                raise AntiSpamException('Antispam detected')
            return self.check_for_translation()

        self.WEBDRIVER_WAIT(self._driver, 10).until(wait_for)

    @staticmethod
    def clear(data: str) -> str:
        paragraphs = data.split('\n')
        paragraphs = [paragraph.strip() for paragraph in paragraphs]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        return '\n'.join(paragraphs)

    @staticmethod
    def build_params(params: dict[str, str]) -> str:
        return urllib.parse.urlencode(params)
