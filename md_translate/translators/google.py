from ._base import TranslationProvider


class GoogleTranslateProvider(TranslationProvider):  # pragma: no cover
    HOST = 'https://translate.google.com/'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'sl': from_language,
            'tl': to_language,
        }
        self._driver.get(self.get_url(params))
        self.cookies_accept()
        textarea = self._driver.find_element(by=self.WEBDRIVER_BY.TAG_NAME, value='textarea')
        result_container = self._driver.find_element(
            by=self.WEBDRIVER_BY.XPATH, value='//div[@aria-live="polite"]'
        )
        textarea.send_keys(text)
        self.WEBDRIVER_WAIT(self._driver, 10).until(lambda driver: result_container.text != '')
        result_element = result_container.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR, value=f'span[lang="{to_language}"]'
        )
        data = result_element.text
        return self.get_cleaned_data(data)

    def check_for_antispam(self) -> bool:
        return False
