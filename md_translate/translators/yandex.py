from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from ._base import TranslationProvider


class YandexTranslateProvider(TranslationProvider):
    HOST = 'https://translate.yandex.com/'

    COOKIES_ACCEPT_BTN_TEXT = 'Accept'

    def get_url(self) -> str:
        params = {
            'lang': f'{self.from_language}-{self.to_language}',
        }
        return f'{self._host}?{self.build_params(params)}'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.CLASS_NAME, value='textinput')

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='translation')

    def check_for_translation(self) -> bool:
        try:
            container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='textbox2')
            if 'fetching' in container.get_attribute('class'):
                return False
            element = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='translation')
            return element.text != ''
        except NoSuchElementException:
            return False

    def accept_cookies(self) -> None:
        self.click_cookies_accept('Accept')

    def check_for_antispam(self) -> bool:
        try:
            self._driver.find_element(
                by=self.WEBDRIVER_BY.XPATH,
                value='//*[text()="Please confirm that you and not a robot are sending requests"]',
            )
            return True
        except Exception:
            return 'showcaptcha' in self._driver.current_url
