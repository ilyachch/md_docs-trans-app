#!/bin/bash

cd "$(dirname "$0")"

# install Python packages
# The pyvenv script has been deprecated as of Python 3.6 in favor of using python3 -m venv. https://docs.python.org/3/library/venv.html
if [[ -x /usr/bin/python3.6 ]] ; then
    PYTHON3=/usr/bin/python3.6
    sudo apt-get install python3.6-venv -y
else
    if [ -x /usr/bin/python3.5 ] ; then
        PYTHON3=/usr/bin/python3.5
        sudo apt-get install python3.5-venv -y
    else
        PYTHON3=/usr/bin/python3
        sudo apt-get install python3-venv -y
    fi
fi

PIP=venv/bin/pip
LOC_PYTHON=venv/bin/python

echo "TEMP_API_KEY" > "TRANSLATE_API_KEY"

${PYTHON3} -m venv venv
${PIP} install pip --upgrade
${PIP} install setuptools --upgrade
${PIP} install --upgrade --upgrade-strategy only-if-needed -r requirements.txt
