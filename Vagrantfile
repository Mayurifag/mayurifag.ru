# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_version ">= 2.2"

Vagrant.configure("2") do |config|
  config.vm.hostname = 'mayurifag.local'
  config.vm.network 'private_network', ip: '172.16.100.2'

  config.vm.provision :ansible do |ansible|
    ansible.galaxy_role_file = 'provisioning/requirements.yml'
    ansible.playbook = 'provisioning/setup.yml'
    ansible.host_key_checking = false
    # ansible.verbose = 'vvvv'
  end

  config.vm.provider :virtualbox do |v|
    v.memory = 512
  end

  config.vm.box = "geerlingguy/debian9"

  # config.vm.network "forwarded_port", guest: 22, host: 10022
  # config.vm.network "forwarded_port", guest: 25, host: 10025
  # config.vm.network "forwarded_port", guest: 80, host: 10080
  # config.vm.network "forwarded_port", guest: 443, host: 10443
  # config.vm.network "forwarded_port", guest: 993, host: 10993


  # config.vm.network "forwarded_port", guest:  25, host: 1025 # SMTP
  # config.vm.network "forwarded_port", guest: 143, host: 1143 # IMAP
  # config.vm.network "forwarded_port", guest: 993, host: 1993 # IMAPS

  # config.vm.network "forwarded_port", guest: 7777, host: 7777
  # config.vm.network "forwarded_port", guest: 8888, host: 8888
  config.vm.network "forwarded_port", guest: 51820, host: 51820
end
