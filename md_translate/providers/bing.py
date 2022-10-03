from md_translate.providers._base import Provider


class BingTranslateProvider(Provider):
    def translate(self, from_language: str, to_language: str, text: str) -> str:
        pass
