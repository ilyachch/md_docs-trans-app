# MD Translate

CLI tool to translate `.md` files from English to Russian.


Can use Yandex Translation API and Google Cloud translation.

## Installation

Install project:

```bash
$ pip install md-translate
```

Create a file, named `.md_translate_api_key` in your home folder or wherever you want put your API key into it.


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

It will find all `.md` files in folder you set and line by line, will translate. It will translate only paragraphs, not lists or any other markdown constructions.
