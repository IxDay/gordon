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
    deactivate
    cd "$TOP_DIR"
    git clone "https://github.com/RulzUrLife/""$MODULE"
    cd "$MODULE"
    bash install.sh
  done
}

main () {
  repositories_initialization
}

main
