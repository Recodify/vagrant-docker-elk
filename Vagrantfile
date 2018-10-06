# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.vm.box = "williamyeh/ubuntu-trusty64-docker"

  config.vm.network :private_network, :ip => '10.0.1.2'

  # nginx
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Rabbit
  config.vm.network "forwarded_port", guest: 15672, host: 15672
  config.vm.network "forwarded_port", guest: 5672, host: 5672

  # cAdvisor
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  # ElasticSearch
  config.vm.network "forwarded_port", guest: 9200, host: 9200

  config.vm.synced_folder "./", "/playbook", owner: "vagrant",
    group: "vagrant", mount_options: ["dmode=775,fmode=664"]

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install software-properties-common -y
    sudo apt-add-repository ppa:ansible/ansible -y
    sudo apt-get update
    sudo apt-get install ansible -y
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    docker run -d --hostname rabbit --name rabbit -p 15672:15672 rabbitmq:3-management
  SHELL
end
