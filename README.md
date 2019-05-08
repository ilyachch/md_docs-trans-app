# MD Translate

CLI tool to translate `.md` files from English to Russian.


Can use Yandex Translation API and Google Cloud translation.

## Installation

Install project:

```bash
$ pip install md-translate
```

Create a file, named `.md_translate_api_key` in your home folder or wherever you want put your API key into it.

## Settings file

You can store your default settings in `.ini` file.

By default, place for settings file is `~/.md_translate_config.ini`, but you can place it wherever you want.

Settings file content example:
```.ini
[Settings]
# (would be changed to store exactly API KEY)
api_key = <path to api_key file> 
service = Yandex
source_lang = en
target_lang = ru

```

## Using

To run translation:

```bash
$ md-translate path_to_folder_with_md_files
```

Arguments:

* `-k (--api_key) path_to_api_key_file` (if you put api key file not to home folder)
* `-s (--service) [Yandex, Google]` service to be used for translation
* `-S (--source_lang) land_code` language code of source document (default: 'en')
* `-T (--target_lang) lang_code` language code to translate in (default: 'ru')

If you made settings file, run it with this arguments:

* `-c (--config_path) path_to_config_file` (If it is not in your home directory)
* `-C (--use_config)` (Yes, it's boolean. Use it if file is named `.md_translate_config.ini` and it placed in your home dir)

It will find all `.md` files in folder you set and line by line, will translate. It will translate only paragraphs, not lists or any other markdown constructions.
