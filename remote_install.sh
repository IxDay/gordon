#!/bin/bash
set -e

PROJECT="RulzUrArch"

command -v git > /dev/null || ( echo "git is not installed, aborting..." && exit 1 )
command -v vagrant > /dev/null || ( echo "vagrant is not installed, aborting..." && exit 1 )

git clone "https://github.com/RulzUrLife/""$PROJECT"
cd "$PROJECT"

vagrant up
vagrant ssh -c /vagrant/install.sh
vagrant ssh
