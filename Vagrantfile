# -*- mode: ruby -*-
 # vi: set ft=ruby :

 Vagrant.configure("2") do |config|
     config.vm.box = "docker"
     config.vm.box_url = "http://files.maur.12.lc/docker.box"
     config.vm.provider "virtualbox" do |v|
         v.customize ["modifyvm", :id, "--memory", "2048"]
         v.customize ["modifyvm", :id, "--cpus", "2"]
     end
     config.vm.network :private_network, ip: "192.168.56.4"
 end
