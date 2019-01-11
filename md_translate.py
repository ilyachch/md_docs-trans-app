import argparse
import pathlib

from md_translate.files_worker import FilesWorker


class App:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = self.__process_args()
        self.file_worker = FilesWorker(self.args.path)

    def __process_args(self):
        self.parser.add_argument('-p', '--path',
                                 help='Path to folder to process.',
                                 dest='path', type=pathlib.Path)
        return self.parser.parse_args()

    def process(self):
        self.file_worker.process()


if __name__ == "__main__":
    app = App()
    app.process()
