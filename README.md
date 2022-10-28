# MD Translate

CLI tool to translate `.md` files.

Can use Google, Yandex, Deepl, Bing. Requires chrome webdriver to run.

## Installation

Install project (pipx is recommended):

```bash
$ pipx install md-translate
```

## Usage

```bash
$ md-translate --help

Usage: md-translate [OPTIONS] PATH

Options:
  -F, --from-lang TEXT            Source language code  [required]
  -T, --to-lang TEXT              Target language code  [required]
  -P, --service [yandex|google|bing|deepl]
                                  Translating service  [required]
  -N, --new-file                  Create new file with translated content
  -I, --ignore-cache              Ignore cache
  -S, --save-temp-on-complete     Save temp files on complete.
  -O, --overwrite                 Overwrite existing files.
  -v, --verbose
  --help                          Show this message and exit.
```

`Path` can be a file or a directory. If it's a directory, all `.md` files will be translated.
