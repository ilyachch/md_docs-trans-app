import urllib.parse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from md_translate.providers._base import Provider


class BingTranslateProvider(Provider):
    HEADLESS = False

    def __init__(self):
        super().__init__()
        self._host = 'https://www.bing.com/translator/'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'from': from_language,
            'to': to_language,
        }
        url = f'{self._host}?{urllib.parse.urlencode(params)}'
        self._driver.get(url)
        text_area = self._driver.find_element(by=By.ID, value='tta_input_ta')

        result_container = self._driver.find_element(by=By.ID, value='tta_output_ta')

        current_text = result_container.get_attribute('value')

        text_area.send_keys(text)

        def wait_for_text(driver):
            new_text = driver.find_element(by=By.ID, value='tta_output_ta').get_attribute('value')
            if new_text not in [current_text, '...', ' ...']:
                return True
            return False

        WebDriverWait(self._driver, 10).until(wait_for_text)

        data = result_container.get_attribute('value')
        data = data.strip()
        data = data.replace('\n ', '  ')
        return data
