from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from ._base import TranslationProvider


class DeeplTranslateProvider(TranslationProvider):
    HOST = 'https://www.deepl.com/translator/'

    def get_url(self) -> str:
        return f'{self._host}l/{self.from_language}/{self.to_language}/'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='textarea[aria-labelledby="translation-source-heading"]',
        )

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='textarea[aria-labelledby="translation-results-heading"]',
        )

    def check_for_translation(self) -> bool:
        try:
            container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='dl_translator')
            return 'lmt--active_translation_request' not in container.get_attribute('class')
        except NoSuchElementException:
            return False

    def accept_cookies(self) -> None:
        self.click_cookies_accept('Accept')

    def click_cookies_accept(self, btn_text: str) -> None:
        try:
            cookies_accept_button = self._driver.find_element(
                by=self.WEBDRIVER_BY.CLASS_NAME, value='dl_cookieBanner--buttonAll'
            )
            if cookies_accept_button:
                cookies_accept_button.click()
        except NoSuchElementException:
            return

    def check_for_antispam(self) -> bool:
        return False

    @staticmethod
    def get_translated_data(output_element: WebElement) -> str:
        return output_element.get_attribute('value')
