class MdTranslateBaseException(Exception):
    def get_message(self):
        raise NotImplementedError()


class ConfigurationError(MdTranslateBaseException):
    def get_message(self):
        return 'Some of settings missed. Check your config file'


class ObjectNotFoundException(MdTranslateBaseException):
    def __init__(self, obj):
        self.object = obj

    def get_message(self):
        '{} not found'.format(self.object)


class NoApiKeyFileError(MdTranslateBaseException):
    def __init__(self, api_key_path):
        self.api_key_path = api_key_path

    def get_message(self):
        return ('API_KEY file in location "{}" not found\n'
                'Provide API_KEY file path or create it, if not exist').format(self.api_key_path)


class NoConfigFileError(MdTranslateBaseException):
    def __init__(self, not_found_file):
        self.not_found_file = not_found_file

    def get_message(self):
        return 'No config file found. Create file {} or pass custom file  with `-c` param'.format(self.not_found_file)


class FileIsNotMarkdown(MdTranslateBaseException):
    def __init__(self, not_md_obj):
        self.not_md_obj = not_md_obj

    def get_message(self):
        return '{} is not a Markdown file!'.format(self.not_md_obj)
