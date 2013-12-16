#!/bin/bash
set -e

PROJECT="RulzUrArch"

command -v git > /dev/null || brew install git 2> /dev/null || sudo apt-get install -y git
git clone "https://github.com/RulzUrLife/""$PROJECT"
cd "$PROJECT"
./install.sh
