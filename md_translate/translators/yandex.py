from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from md_translate.exceptions import safe_run

from ._selenium_base import SeleniumBaseTranslator


class YandexTranslateProvider(SeleniumBaseTranslator):
    HOST = 'https://translate.yandex.com/'

    COOKIES_ACCEPT_BTN_TEXT = 'Accept'

    def get_url(self) -> str:
        params = {
            'lang': f'{self.from_language}-{self.to_language}',
        }
        return f'{self.HOST}?{self.build_params(params)}'

    def get_input_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.CLASS_NAME, value='textinput')

    def get_output_element(self) -> WebElement:
        return self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='translation')

    @safe_run(NoSuchElementException, default_return_value=False)
    def check_for_translation(self) -> bool:
        container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='textbox2')
        if 'fetching' in container.get_attribute('class'):
            return False
        element = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='translation')
        return element.text != ''

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
