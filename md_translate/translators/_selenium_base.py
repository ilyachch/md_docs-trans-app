import abc
import logging
import pathlib
import time
import urllib.parse
from typing import TYPE_CHECKING, Any, Optional

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from md_translate.translators._base_translator import BaseTranslator
from md_translate.translators.randomizer.randomizer import Randomizer

if TYPE_CHECKING:
    from md_translate.settings import Settings

current_dir = pathlib.Path(__file__).parent.absolute()
logger = logging.getLogger(__name__)


class AntiSpamException(Exception):
    pass


class SeleniumBaseTranslator(BaseTranslator):
    HEADLESS = False

    WEBDRIVER_WAIT = WebDriverWait
    WEBDRIVER_BY = By

    HOST: Optional[str] = None

    COOKIES_ACCEPT_BTN_TEXT = 'Accept all'

    ANTISPAM_TIMEOUT = 60 * 60  # 1 hour
    PAGE_LOAD_TIMEOUT = 10
    TRANSLATION_TIMEOUT = 10

    def __init__(self, settings: 'Settings') -> None:
        self._settings = settings
        self._session = requests.Session()
        self.from_language = settings.from_lang
        self.to_language = settings.to_lang
        self.randomizer = Randomizer()

    def __enter__(self) -> 'BaseTranslator':
        options = self.randomizer.make_options()
        self._driver = webdriver.Chrome(  # type: ignore
            service=ChromeService(ChromeDriverManager(version='latest').install()), options=options
        )
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

        self.WEBDRIVER_WAIT(self._driver, self.PAGE_LOAD_TIMEOUT).until(wait_for)

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
        logger.warning('Waiting for antispam')
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

        self.WEBDRIVER_WAIT(self._driver, self.TRANSLATION_TIMEOUT).until(wait_for)

    @staticmethod
    def clear(data: str) -> str:
        paragraphs = data.split('\n')
        paragraphs = [paragraph.strip() for paragraph in paragraphs]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        return '\n'.join(paragraphs)

    @staticmethod
    def build_params(params: dict[str, str]) -> str:
        return urllib.parse.urlencode(params)
