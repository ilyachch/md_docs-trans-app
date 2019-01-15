# MD Translate

CLI to translate `.md` files from English to Russian.

Uses Yandex Translation API.

## Installation

To use, make `clone` and then `./install.sh`. It will check installed Python version, install, venv, create venv and create file `TRANSLATE_API_KEY`. There you should put your API Key, you got from (Yandex)[https://translate.yandex.ru/developers/keys].

## Using

To start translation, you should activate venv, by `source venv/bin/activate` and then you can use run it by `python md_translate.py -p <PATH TO FOLDER>`.

It will find all `.md` files in folder you set and line by line, will translate. It will translate only paragraphs, not lists or any other markdown constructions.

## Plans to extend

* Make it translate all needed text blocks, not only paragraphs;
* Make it translate not only "English" -> "Russian";