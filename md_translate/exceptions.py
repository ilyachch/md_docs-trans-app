class ConfigurationError(RuntimeError):
    pass


class DirectoryNotFoundException(OSError):
    pass


class NoApiKeyFileError(RuntimeError):
    pass


class NoConfigFileError(RuntimeError):
    pass
