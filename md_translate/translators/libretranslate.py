from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from md_translate.exceptions import safe_run

from ._selenium_base import SeleniumBaseTranslator


class LibreTranslateTranslateProvider(SeleniumBaseTranslator):
    HOST = 'https://libretranslate.com/'

    def get_url(self) -> str:
        params = {
            'source': self.from_language,
            'target': self.to_language,
        }
        return f'{self.HOST}?{self.build_params(params)}'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='textarea1')

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='textarea2')

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_translation(self) -> bool:
        element = self.get_output_element()
        return element.get_attribute('value') != ''

    def accept_cookies(self) -> None:
        return

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_antispam(self) -> bool:
        container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='t_enter_captcha')
        return container.is_displayed()

    @staticmethod
    def get_translated_data(output_element: WebElement) -> str:
        return output_element.get_attribute('value')

    def wait_for_page_load(self) -> None:
        def wait_for(driver: Any) -> bool:
            document_ready = driver.execute_script('return document.readyState') == 'complete'
            controls_loaded = (
                len(driver.find_elements(by=self.WEBDRIVER_BY.ID, value='textarea1')) > 0
            )
            return document_ready and controls_loaded

        self.WEBDRIVER_WAIT(self._driver, self.PAGE_LOAD_TIMEOUT).until(wait_for)
