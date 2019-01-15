# MD Translate

CLI to translate `.md` files from English to Russian.

Uses Yandex Translation API.

## Installation

Get project and install by: 

```bash
$ git clone git@github.com:ilyachch/docs-trans-app.git
$ cd docs-trans-app
$ ./install.sh
```

It will check installed Python version, install venv, create venv, load requirements and create file `TRANSLATE_API_KEY` with some dummy. There you should put your API Key, you got from [Yandex Translate](https://translate.yandex.ru/developers/keys).

## Using

To start translation, you should activate venv, by `source venv/bin/activate` and then you can use run it by `python md_translate.py -p <PATH TO FOLDER>`.

It will find all `.md` files in folder you set and line by line, will translate. It will translate only paragraphs, not lists or any other markdown constructions.

## Plans to extend

* Make it translate all needed text blocks, not only paragraphs;
* Make it translate not only "English" -> "Russian";
* Make it translate using not only Yandex Translation API;
