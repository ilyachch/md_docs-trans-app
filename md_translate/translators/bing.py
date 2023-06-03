from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from md_translate.exceptions import safe_run

from ._selenium_base import SeleniumBaseTranslator


class BingTranslateProvider(SeleniumBaseTranslator):
    HOST = 'https://www.bing.com/translator/'

    def get_url(self) -> str:
        params = {
            'from': self.from_language,
            'to': self.to_language,
        }
        return f'{self.HOST}?{self.build_params(params)}'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='tta_input_ta')

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='tta_output_ta')

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_translation(self) -> bool:
        container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='rich_tta')
        return 'ttastable' in container.get_attribute('class')

    def accept_cookies(self) -> None:
        self.click_cookies_accept('Accept')

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_antispam(self) -> bool:
        container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='t_enter_captcha')
        return container.is_displayed()

    @staticmethod
    def get_translated_data(output_element: WebElement) -> str:
        return output_element.get_attribute('value')
