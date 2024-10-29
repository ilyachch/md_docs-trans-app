from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from md_translate.exceptions import safe_run

from ._selenium_base import SeleniumBaseTranslator


class DeeplTranslateProvider(SeleniumBaseTranslator):
    HOST = 'https://www.deepl.com/translator/'

    TRANSLATION_TIMEOUT = 30

    def get_url(self) -> str:
        return f'{self.HOST}l/{self.from_language}/{self.to_language}/'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='d-textarea[name="source"]',
        )

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='d-textarea[name="target"]',
        )

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_translation(self) -> bool:
        element = self.get_output_element()
        return element.text != ''

    def accept_cookies(self) -> None:
        self.click_cookies_accept('Accept')

    @safe_run(NoSuchElementException, default_return_value=None)
    def click_cookies_accept(self, btn_text: str) -> None:
        cookies_accept_button = self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='[data-testid="cookie-banner-strict-accept-all"]',
        )
        if cookies_accept_button:
            cookies_accept_button.click()

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_antispam(self) -> bool:
        container = self._driver.find_element(
            by=self.WEBDRIVER_BY.XPATH,
            value='//*[text()="You’ve reached your free usage limit.*"]',
        )
        return container.is_displayed()

    @staticmethod
    def get_translated_data(output_element: WebElement) -> str:
        return output_element.get_attribute('value')
