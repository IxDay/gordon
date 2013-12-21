#!/bin/bash
set -e

command -v VBoxManage > /dev/null || ( echo "VirtualBox is not installed, aborting..." && exit 1 )
command -v vagrant > /dev/null || ( echo "Vagrant is not installed, aborting..." && exit 1 )
command -v curl > /dev/null || ( echo "curl is not installed, aborting..." && exit 1 )

if [ "$(ls -A .)" ]; then
    mkdir RulzUrKitchen
    cd RulzUrKitchen
fi

curl https://raw.github.com/RulzUrLife/RulzUrArch/master/Vagrantfile -o Vagrantfile
vagrant up

# Due to the installation of VirtualBox guest additions during the provisioning,
# a reboot of the Vagrant box is needed.
vagrant halt
vagrant up

# Removing the file before git clone prevent the fail on non empty directories
vagrant ssh -c "cd /vagrant; rm Vagrantfile; git init; git remote add origin https://github.com/RulzUrLife/RulzUrArch; git fetch; git checkout -t origin/master"
