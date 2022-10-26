from md_translate.translators._base import TranslationProvider


class YandexTranslateProvider(TranslationProvider):  # pragma: no cover
    HOST = 'https://translate.yandex.com/'

    COOKIES_ACCEPT_BTN_TEXT = 'Accept'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        params = {
            'lang': f'{from_language}-{to_language}',
        }
        self._driver.get(self.get_url(params))
        self.wait_for_page_load()
        if self.check_for_antispam():
            self.wait_for_antispam()
        textarea = self._driver.find_element(by=self.WEBDRIVER_BY.CLASS_NAME, value='textinput')
        result_container = self._driver.find_element(by=self.WEBDRIVER_BY.ID, value='textbox2')
        textarea.send_keys(text)
        if self.check_for_antispam():
            self.wait_for_antispam()

        self.WEBDRIVER_WAIT(self._driver, 10).until(lambda driver: result_container.text != '')
        data = result_container.text
        return self.get_cleaned_data(data)

    def check_for_antispam(self) -> bool:
        try:
            self._driver.find_element(
                by=self.WEBDRIVER_BY.XPATH,
                value='//*[text()="Please confirm that you and not a robot are sending requests"]',
            )
            return True
        except Exception:
            return 'showcaptcha' in self._driver.current_url
