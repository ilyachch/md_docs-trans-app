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
        except NoApiKeyFileError as err:
            print(err.get_message())
            exit(1)

    def process(self):
        FilesWorker(self.settings.path).process()


def main():
    try:
        App().process()
        exit(0)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":
    main()
