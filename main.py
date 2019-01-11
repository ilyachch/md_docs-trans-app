import argparse
import os
import pathlib
import re
from urllib.parse import urlencode

import requests


class App:
    source_lang = 'en'
    target_lang = 'ru'

    DEFAULT_API_KEY_FILE = 'APIKEY'

    base_api_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.API_KEY = self.__get_api_key()
        self.args = self.__process_args()
        self.path = self.args.path
        self.list_of_files = self.__get_list_of_files_by_path()
        self.request_url = self.__build_url()

    def __process_args(self):
        self.parser.add_argument('-p', '--path',
                                 help='Path to folder to process.',
                                 dest='path', type=pathlib.Path)
        self.parser.add_argument('-k', '--key',
                                 help='Api key file name.',
                                 dest='api_key', type=str, required=False, default=None)
        return self.parser.parse_args()

    def __get_api_key(self):
        key_file_name = self.args.get('key', self.DEFAULT_API_KEY_FILE)
        if not os.path.exists(key_file_name):
            raise FileNotFoundError('Not found {} file with Yandex API key.'.format(key_file_name))
        with open(key_file_name) as api_key_file:
            return api_key_file.read()

    def __get_list_of_files_by_path(self):
        md_files = []
        if not os.path.exists(self.path):
            raise FileNotFoundError('No such folder: {}.'.format(self.path))
        for link in os.listdir(self.path):
            if link.endswith('.md'):
                md_files.append(link)
        if len(md_files) == 0:
            raise FileNotFoundError('No MD files in provided path found.')
        return md_files

    def __build_url(self):
        query_string = urlencode({
            'key': self.API_KEY,
            'lang': '{source}-{target}'.format(source=self.source_lang, target=self.target_lang),
        })
        return '?'.join([self.base_api_url, query_string])

    def process(self):
        for file_name in self.list_of_files:
            print('Processing file: {}'.format(file_name))
            with open(os.path.join(self.path, file_name), 'r+') as md_file:
                translated = self.__process_file(md_file)
                self.__write_translated_data_to_file(md_file, translated)

    def __process_file(self, md_file):
        lines = md_file.readlines()
        lines_with_translation = []
        code_block = False
        for counter, line in enumerate(lines):
            lines_with_translation.append(line)
            if line.startswith('```') and len(line) == 3:
                code_block = not code_block
            if line.startswith('```') and line.endswith('```') and len(line) > 3:
                continue
            if not re.match("^[a-zA-Z]+.*", line) or code_block:
                continue
            translated_line = self.__request_translation(line)
            lines_with_translation.append('\n')
            lines_with_translation.append(translated_line)

            print('Processed: {counter} lines of {total}.'.format(
                counter=counter,
                total=len(lines)
            ))

        return lines_with_translation

    def __request_translation(self, data_string):
        req = requests.post(self.request_url, {'text': data_string})
        raw_translation = req.json()['text']
        translation = '\n'.join(raw_translation)
        return translation

    def __write_translated_data_to_file(self, md_file, translated_data):
        md_file.seek(0)
        for line in translated_data:
            md_file.writelines(line)


if __name__ == "__main__":
    app = App()
    app.process()
