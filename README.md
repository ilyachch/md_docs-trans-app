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

## Usage

```bash
$ app.py [-h] [-c CONFIG_PATH] [-k API_KEY_FILE | -K API_KEY]
              [-s {Yandex,Google}] [-S SOURCE_LANG] [-T TARGET_LANG]
              [path]
```

If you set config file, you can override any of settings by arguments

### Positional arguments:
* `path` Path to folder to process. If not set, uses current folder

### Optional arguments:
* `-h, --help`, show this help message and exit
* `-c CONFIG_PATH, --config_path CONFIG_PATH`, Path to config_file
* `-k API_KEY_FILE, --api_key_file API_KEY_FILE`, Path to Translation Service API key file
* `-K API_KEY, --api_key API_KEY`, API key to use Translation API
* `-s {Yandex,Google}, --service {Yandex,Google}`, Translating service
* `-S SOURCE_LANG, --source_lang SOURCE_LANG`, Source language
* `-T TARGET_LANG, --target_lang TARGET_LANG`, Target language

