class ConfigurationError(RuntimeError):
    pass


class DirectoryNotFoundException(OSError):
    pass


class NoApiKeyFileError(RuntimeError):
    def __init__(self, api_key_path):
        self.api_key_path = api_key_path

    def get_message(self):
        return ('API_KEY file in location "{}" not found\n'
                'Provide API_KEY file path or create it, if not exist').format(self.api_key_path)


class NoConfigFileError(RuntimeError):
    pass
