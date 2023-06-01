# Markdown Docs Translator

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

Markdown Docs Translator is an automated translator for markdown documents, built with Python. The tool supports multiple translation services and provides a variety of options to customize the translation process.

## Features
- Support for multiple translation services (Yandex, Google, Bing, Deepl).
- Multithreading for faster translations.
- Options to overwrite original files, drop original files, or create a new file with translated text.
- Caching for faster repeat translations.
- Verbosity level control.

## Installation

### From PyPI (highly recommended to use pipx):
```bash
```bash
pipx install md-translate
```

### Git:
```bash
git clone https://github.com/ilyachch/md_docs-trans-app.git
cd md_docs-trans-app
pip install .
```

## Usage
```bash
md-translate path_to_file_or_folder -F source_lang -T target_lang -P service [OPTIONS]
```
Where:
- `path_to_file_or_folder` is the path to the markdown file or folder containing markdown files to translate.
- `source_lang` is the language code of the source document.
- `target_lang` is the language code for the translation.
- `service` is the translating service to use (yandex, google, bing, deepl).
- `OPTIONS` are additional options that can be specified as listed below.

### Options
| Option                        | Description                          |
|-------------------------------|--------------------------------------|
| `-F, --from-lang TEXT`        | Source language code [required]      |
| `-T, --to-lang TEXT`          | Target language code [required]      |
| `-P, --service`               | Translating service [required]       |
| `-X, --processes INTEGER`     | Number of processes to use           |
| `-N, --new-file`              | Create new file with translated text |
| `-I, --ignore-cache`          | Ignore cache                         |
| `-S, --save-temp-on-complete` | Save temporary files on complete     |
| `-O, --overwrite`             | Overwrite original files             |
| `-V, --verbose`               | Verbosity level                      |
| `-D, --drop-original`         | Drop original files                  |
| `--help`                      | Show help message and exit           |

Currently supported services are:
- `Yandex`
- `Google`
- `Bing`
- `Deepl`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
