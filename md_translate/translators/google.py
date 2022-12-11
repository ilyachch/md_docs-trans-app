from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from ._base import TranslationProvider


class GoogleTranslateProvider(TranslationProvider):
    HOST = 'https://translate.google.com/'

    def get_url(self) -> str:
        params = {
            'sl': self.from_language,
            'tl': self.to_language,
        }
        return f'{self._host}?{self.build_params(params)}'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR, value=f'span[lang="{self.from_language}"]'
        ).find_element(by=self.WEBDRIVER_BY.TAG_NAME, value='textarea')

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(
            by=self.WEBDRIVER_BY.XPATH, value='//div[@aria-live="polite"]'
        ).find_element(by=self.WEBDRIVER_BY.CSS_SELECTOR, value=f'span[lang="{self.to_language}"]')

    def check_for_translation(self) -> bool:
        try:
            element = self.get_output_element()
            return element.text != ''
        except NoSuchElementException:
            return False

    def accept_cookies(self) -> None:
        if 'consent.google.com' in self._driver.current_url:
            buttons = self._driver.find_elements(by=self.WEBDRIVER_BY.TAG_NAME, value='button')
            buttons[1].click()

    def check_for_antispam(self) -> bool:
        try:
            element = self._driver.find_element(
                by=self.WEBDRIVER_BY.XPATH, value='//div[text()="Translation error"]'
            )
            parent = element.find_element(by=self.WEBDRIVER_BY.XPATH, value='..')
            return parent.is_displayed()
        except NoSuchElementException:
            return False
