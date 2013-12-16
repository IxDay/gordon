#!/bin/sh

set -e

MODULES=("RulzUrAPI")
TOP_DIR=$(cd $(dirname "$0") && pwd)

check_virtualenv () {
	if [[ -z "$VIRTUAL_ENV" ]]
	then
    echo "your are not in a dedicated virtualenv, aborting..."
    exit 1
	fi
}

git_clone () {
  cd "$TOP_DIR"
  for MODULE in "${MODULES[@]}"
  do
    git clone "https://github.com/RulzUrLife/""$MODULE"
  done
}

pip_install () {
  check_virtualenv
  pip install -r "$TOP_DIR""/requirements.txt"
}

main () {
  git_clone
  pip_install
}

main
