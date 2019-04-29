from md_translate.arguments_processor import settings
from md_translate.exceptions import NoApiKeyFileError
from md_translate.files_worker import FilesWorker


class App:
    def __init__(self):
        self.settings = settings
        self.__validate_setup()

    def __validate_setup(self):
        try:
            self.settings.validate_arguments()
        except NoApiKeyFileError:
            print('API_KEY file in location "{}" not found'.format(self.settings.api_key))
            print('Provide API_KEY file path or create it, if not exist')
            print()
            self.settings.arg_parser.print_help()
            exit(1)

    def process(self):
        FilesWorker(self.settings.path).process()


if __name__ == "__main__":
    app = App()
    app.process()
