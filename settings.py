class Settings:
    api_key_filename = 'TRANSLATE_API_KEY'

    source_lang = 'en'
    target_lang = 'ru'

    API_KEY_CACHE = None

    @property
    def api_key(self):
        if Settings.API_KEY_CACHE is None:
            with open(Settings.api_key_filename) as api_key_file:
                Settings.API_KEY_CACHE = api_key_file.read()
        return Settings.API_KEY_CACHE

    @property
    def lang_string(self):
        return '{source}-{target}'.format(source=self.source_lang, target=self.target_lang)
