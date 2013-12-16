#!/bin/bash
set -e

PROJECT="RulzUrArch"
MODULES=("RulzUrAPI")
TOP_DIR=$(cd $(dirname "$0") && pwd)

install_packages () {
  VENV=0
  VENV_WRAPPER=0

  command -v git > /dev/null || brew install git 2> /dev/null || sudo apt-get install -y git  
  command -v pip > /dev/null || brew install pip 2> /dev/null || sudo apt-get install -y python-pip  


  if [[ ! $(pip freeze 2> /dev/null | grep virtualenv=) ]]
  then
    echo "install virtualenv"
    pip install virtualenv > /dev/null || sudo pip install virtualenv > /dev/null
  fi

  if [[ ! $(pip freeze 2> /dev/null | grep virtualenvwrapper=) ]]
  then
    echo "install virtualenvwrapper"
    pip install virtualenvwrapper > /dev/null || sudo pip install virtualenvwrapper > /dev/null
    if [[ ! $(grep "virtualenvwrapper" "$HOME/.bashrc") ]]      
    then
      echo "source /usr/local/bin/virtualenvwrapper.sh" >> "$HOME/.bashrc"
    fi    
  fi
  source "/usr/local/bin/virtualenvwrapper.sh"  
}

repositories_initialization () {
  set +e # mkvirtualenv fails with no reason
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
  install_packages
  repositories_initialization  
}

main
