from md_translate.providers._base import TranslationProvider


class BingTranslateProvider(TranslationProvider):
    HOST = 'https://www.bing.com/translator/'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'from': from_language,
            'to': to_language,
        }
        self._driver.get(self.get_url(params))
        text_area = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='tta_input_ta')

        result_container = self._driver.find_element(
            by=self.WEBDRIVER_BY.ID, value='tta_output_ta'
        )

        current_text = result_container.get_attribute('value')

        text_area.send_keys(text)

        def wait_for_text(driver):
            new_text = driver.find_element(
                by=self.WEBDRIVER_BY.ID, value='tta_output_ta'
            ).get_attribute('value')
            if new_text != current_text and '...' not in new_text:
                return True
            return False

        self.WEBDRIVER_WAIT(self._driver, 10).until(wait_for_text)

        data = result_container.get_attribute('value')
        return self.get_cleaned_data(data)
