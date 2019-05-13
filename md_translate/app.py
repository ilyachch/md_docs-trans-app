from md_translate.arguments_processor import settings
from md_translate.exceptions import NoApiKeyFileError
from md_translate.files_worker import FilesWorker
from md_translate.file_translator import FileTranslator


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
        files_to_process = FilesWorker(self.settings.path).get_files_to_translate()
        for file_name in files_to_process:
            with FileTranslator(self.settings, file_name) as processing_file:
                processing_file.translate()
            print('Processed: {file_name}'.format(file_name=file_name))


def main():
    try:
        App().process()
        exit(0)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":
    main()
