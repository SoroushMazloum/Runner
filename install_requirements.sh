#!/bin/bash

set -e

BASHRC_FILE="$HOME/.bashrc"
ACTIVATE_LINE="source $(pwd)/.venv/bin/activate"

python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

