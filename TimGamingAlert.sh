#!/usr/bin/env bash
#set -e
BASEDIR=$(dirname "$BASH_SOURCE")
echo "$BASEDIR"
source "$BASEDIR/venv/bin/activate"
python3 "$BASEDIR/TimGamingAlert.py"