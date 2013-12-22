# -*- mode: ruby -*-
# vi: set ft=ruby :

$install_script = <<INSTALL_SCRIPT

apt-get install -y vim git curl

INSTALL_SCRIPT

# A script to upgrade from the 12.04 kernel to the raring backport kernel (3.8)
# and install docker.
$script = <<SCRIPT
# The username to add to the docker group will be passed as the first argument
# to the script.  If nothing is passed, default to "vagrant".
user="$1"
if [ -z "$user" ]; then
    user=vagrant
fi

# Adding an apt gpg key is idempotent.
wget -q -O - https://get.docker.io/gpg | apt-key add -

# Creating the docker.list file is idempotent, but it may overwrite desired
# settings if it already exists.  This could be solved with md5sum but it
# doesn't seem worth it.
echo 'deb http://get.docker.io/ubuntu docker main' > \
    /etc/apt/sources.list.d/docker.list

# Update remote package metadata.  'apt-get update' is idempotent.
apt-get update -q

# Install docker.  'apt-get install' is idempotent.
apt-get install -q -y lxc-docker

usermod -a -G docker "$user"

tmp=`mktemp -q` && {
    # Only install the backport kernel, don't bother upgrading if the backport is
    # already installed.  We want parse the output of apt so we need to save it
    # with 'tee'.  NOTE: The installation of the kernel will trigger dkms to
    # install vboxguest if needed.
    apt-get install -q -y --no-upgrade linux-image-generic-lts-raring | \
        tee "$tmp"

    # Parse the number of installed packages from the output
    NUM_INST=`awk '$2 == "upgraded," && $4 == "newly" { print $3 }' "$tmp"`
    rm "$tmp"
}

# If the number of installed packages is greater than 0, we want to reboot (the
# backport kernel was installed but is not running).
if [ "$NUM_INST" -gt 0 ];
then
    echo "Rebooting down to activate new kernel."
    echo "/vagrant will not be mounted.  Use 'vagrant halt' followed by"
    echo "'vagrant up' to ensure /vagrant is mounted."
    shutdown -r now
fi
SCRIPT

# We need to install the virtualbox guest additions *before* we do the normal
# docker installation.  As such this script is prepended to the common docker
# install script above.  This allows the install of the backport kernel to
# trigger dkms to build the virtualbox guest module install.
$vbox_script = <<VBOX_SCRIPT + $install_script + $script
# Install the VirtualBox guest additions if they aren't already installed.
if [ ! -d /opt/VBoxGuestAdditions-4.3.4/ ]; then
    # Update remote package metadata.  'apt-get update' is idempotent.
    apt-get update -q

    # Kernel Headers and dkms are required to build the vbox guest kernel
    # modules.
    apt-get install -q -y linux-headers-generic-lts-raring dkms

    echo 'Downloading VBox Guest Additions...'
    wget -cq http://dlc.sun.com.edgesuite.net/virtualbox/4.3.4/VBoxGuestAdditions_4.3.4.iso
    echo "f120793fa35050a8280eacf9c930cf8d9b88795161520f6515c0cc5edda2fe8a  VBoxGuestAdditions_4.3.4.iso" | sha256sum --check || exit 1

    mount -o loop,ro /home/vagrant/VBoxGuestAdditions_4.3.4.iso /mnt
    /mnt/VBoxLinuxAdditions.run --nox11
    umount /mnt
fi
VBOX_SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "docker"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.provider "virtualbox" do |v, override|
    v.name = "RulzUrKitchen"

    override.vm.provision :shell, :inline => $vbox_script
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    v.customize ["modifyvm", :id, "--memory", "2048"]
    v.customize ["modifyvm", :id, "--cpus", "2"]
  end
  config.vm.network :private_network, ip: "192.168.56.4"
end
