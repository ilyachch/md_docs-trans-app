import argparse
import os
import pathlib

from md_translate.exceptions import ConfigurationError
from md_translate.files_worker import FilesWorker
from settings import Settings


class App:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.settings = Settings()
        self.args = self.__process_args()
        self.file_worker = FilesWorker(self.args.path)
        self.__validate_setup()

    def __process_args(self):
        self.parser.add_argument('-p', '--path',
                                 help='Path to folder to process.',
                                 dest='path', type=pathlib.Path)
        return self.parser.parse_args()

    def __validate_setup(self):
        api_key_filename = getattr(self.settings, 'api_key_filename', None)
        if api_key_filename is None:
            raise ConfigurationError('There is no attribute "api_key_filename" in Settings Class.\n'
                                     'Please, check file settings.py in project root.')
        if not os.path.exists(api_key_filename):
            raise ConfigurationError('There is not found file "{filename}"!\n'
                                     'Please, create file with this name and \n'
                                     'put there your API key as plain text \n'
                                     'and restart application'.format(filename=api_key_filename))

    def process(self):
        self.file_worker.process()


if __name__ == "__main__":
    app = App()
    app.process()
