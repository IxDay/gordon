#!/bin/bash

PROJECT="RulzUrArch"
MODULES=("RulzUrAPI")
TOP_DIR=$(cd $(dirname "$0") && pwd)
source "/usr/local/bin/virtualenvwrapper.sh"

repositories_initialization () {
  mkvirtualenv "$PROJECT"
  pip install -r "$TOP_DIR""/requirements.txt"
  for MODULE in "${MODULES[@]}"
  do
    cd "$TOP_DIR"
    git clone "https://github.com/RulzUrLife/""$MODULE"
    cd "$MODULE"
    mkvirtualenv "$MODULE"
    pip install -r "requirements.txt"
  done
}

main () {
  repositories_initialization
}

main
