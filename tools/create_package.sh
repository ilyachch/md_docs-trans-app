#!/usr/bin/env bash

cd "$(dirname "$0")/.."

rm -rf build
rm -rf dist

.venv/bin/python setup.py sdist bdist_wheel
