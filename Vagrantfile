# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_version ">= 2.2"

Vagrant.configure("2") do |config|
  config.vm.hostname = 'mayurifag.local'
  config.vm.network 'private_network', ip: '172.16.100.2'

  # The box does not include provisioners, so include python-apt for ansible working
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get install -y \
      python \
      python-apt
  SHELL

  config.vm.provision :ansible do |ansible|
    ansible.playbook = 'provisioning/setup.yml'
    ansible.host_key_checking = false
    # ansible.verbose = 'vvvv'
  end

  config.vm.provider :virtualbox do |v|
    v.memory = 512
  end

  # vagrant-cachier
  #
  # Install the plugin by running: vagrant plugin install vagrant-cachier
  # More information: https://github.com/fgrehm/vagrant-cachier
  if Vagrant.has_plugin? 'vagrant-cachier'
    config.cache.enable :apt
    config.cache.scope = :box
  end

  config.vm.box = "geerlingguy/debian9"

  # Email
  # config.vm.network "forwarded_port", guest: 22, host: 10022
  # config.vm.network "forwarded_port", guest: 25, host: 10025
  # config.vm.network "forwarded_port", guest: 80, host: 10080
  # config.vm.network "forwarded_port", guest: 443, host: 10443
  # config.vm.network "forwarded_port", guest: 993, host: 10993
  config.vm.network "forwarded_port", guest: 7777, host: 7777
end
