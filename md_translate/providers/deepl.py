from typing import Any

from md_translate.providers._base import TranslationProvider


class DeeplTranslateProvider(TranslationProvider):
    HOST = 'https://www.deepl.com/translator/'

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        url = f'{self._host}l/{from_language}/{to_language}/'
        self._driver.get(url)
        self.cookies_accept()
        textarea = self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='textarea[aria-labelledby="translation-source-heading"]',
        )
        result_container = self._driver.find_element(
            by=self.WEBDRIVER_BY.CSS_SELECTOR,
            value='textarea[aria-labelledby="translation-results-heading"]',
        )
        current_result = result_container.get_attribute('value')
        textarea.send_keys(text)

        def wait_for(driver: Any) -> bool:
            new_result = driver.find_element(
                by=self.WEBDRIVER_BY.CSS_SELECTOR,
                value='textarea[aria-labelledby="translation-results-heading"]',
            ).get_attribute('value')
            if (
                new_result not in [current_result, '']
                and '[...]' not in new_result
                and len(new_result) > len(text) // 2
            ):
                return True
            return False

        self.WEBDRIVER_WAIT(self._driver, 10).until(wait_for)
        data = result_container.get_attribute('value')
        return self.get_cleaned_data(data)
