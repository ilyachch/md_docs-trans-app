from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from ._selenium_base import TranslationProvider


class BingTranslateProvider(TranslationProvider):
    HOST = 'https://www.bing.com/translator/'

    def get_url(self) -> str:
        params = {
            'from': self.from_language,
            'to': self.to_language,
        }
        return f'{self._host}?{self.build_params(params)}'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='tta_input_ta')

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='tta_output_ta')

    def check_for_translation(self) -> bool:
        try:
            container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='rich_tta')
            if 'ttastable' in container.get_attribute('class'):
                return True
            return False
        except NoSuchElementException:
            return False

    def accept_cookies(self) -> None:
        self.click_cookies_accept('Accept')

    def check_for_antispam(self) -> bool:
        try:
            container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='t_enter_captcha')
            return container.is_displayed()
        except NoSuchElementException:
            return False

    @staticmethod
    def get_translated_data(output_element: WebElement) -> str:
        return output_element.get_attribute('value')
