#!/usr/bin/env bash

cd "$(dirname "$0")/.."

.venv/bin/python -m twine upload $1 $2 dist/*
