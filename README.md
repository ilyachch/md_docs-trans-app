# Markdown Docs Translator

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

Markdown Docs Translator is an automated translator for Markdown documents, built with Python. The tool supports multiple translation services and provides a variety of options to customize the translation process.

## Features

- Support for multiple translation services (Yandex, Google, Bing, Deepl).
- Multithreading for faster translations.
- Options to overwrite original files, drop original files, or create a new file with translated text.
- Caching for faster repeat translations.
- Verbosity level control.

## Installation

### From PyPI (highly recommended to use pipx):

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

### Example:

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

| Option                        | Description                                                                                                                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-F, --from-lang TEXT`        | Source language code \[required\]                                                                                                                                                  |
| `-T, --to-lang TEXT`          | Target language code \[required\]                                                                                                                                                  |
| `-P, --service`               | Translating service \[required\]                                                                                                                                                   |
| `-X, --processes INTEGER`     | Number of processes to use. Will be applied to each file separately                                                                                                                |
| `-N, --new-file`              | Create a new file with translated text (original file will remain unchanged). The new file will be created in the same directory as the original file with a "\_translated" suffix |
| `-I, --ignore-cache`          | Ignore cache files. If cache exists, it will be overwritten                                                                                                                        |
| `-S, --save-temp-on-complete` | Save cache files upon completion. If not set, they will be deleted                                                                                                                 |
| `-O, --overwrite`             | Already translated files will be overwritten. Otherwise, these files will be skipped                                                                                               |
| `-D, --drop-original`         | Remove original lines from translated file. These lines will be replaced with translated ones                                                                                      |
| `-V, --verbose`               | Verbosity level                                                                                                                                                                    |
| `--help`                      | Show help message and exit                                                                                                                                                         |

Currently supported services are:

- `Yandex`
- `Google`
- `Bing`
- `Deepl`

### Configuring with a Configuration File

Options for the application can be defined through a configuration file as well. This file should be named `settings.json` and is typically located at `~/.config/md_translate`.

If you choose to use a non-default location for the config file, you can specify its path using the `--config` or `-C` option.

This configuration file can encompass all CLI options except `path`, `from_lang`, `to_lang`, `service` and `config_file_path`. These particular options need to be stated directly in the CLI.

The configuration file should be a valid JSON file and adhere to the following structure:

```json
{
    "processes": 4,
    "new_file": true,
    "ignore_cache": false,
    "save_temp_on_complete": false,
    "overwrite": false,
    "verbose": 1,
    "drop_original": false
}
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
