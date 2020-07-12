[![codecov](https://codecov.io/gh/ilyachch/md_docs-trans-app/branch/master/graph/badge.svg)](https://codecov.io/gh/ilyachch/md_docs-trans-app)
# MD Translate

CLI tool to translate `.md` files from English to Russian and back.

Can use Yandex Translation API and Google Cloud translation.

## Installation

Install project:

```bash
$ pip install md-translate
```

## Settings file

You can store your default settings in `.json` file.

Settings file content example:
```.json
{
  "source_lang": "ru",
  "target_lang": "en",
  "service_name": "Google",
  "api_key": "API_KEY_IN_FILE"
}
```

If you set config file, you should specify it with `-c CONFIG_PATH` argument!

## Usage

```bash
$ md-translate [-h] [-c CONFIG_PATH] [-K API_KEY]
               [-s {Yandex,Google}] [-S {ru, en}] [-T {ru, en}]
               [path]
```

If you set config file, you can override any of settings by arguments

### Positional arguments:
* `path` Path to folder to process. If not set, uses current folder

### Optional arguments:
* `-h, --help`, show this help message and exit
* `-c CONFIG_PATH, --config_path CONFIG_PATH`, Path to config_file
* `-K API_KEY, --api_key API_KEY`, API key to use Translation API
* `-s {Yandex,Google}, --service_name {Yandex,Google}`, Translating service
* `-S SOURCE_LANG, --source_lang SOURCE_LANG`, Source language
* `-T TARGET_LANG, --target_lang TARGET_LANG`, Target language
