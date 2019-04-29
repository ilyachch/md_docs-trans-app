#!/usr/bin/env bash

cd "$(dirname "$0")/.."

bumpversion $1 VERSION
