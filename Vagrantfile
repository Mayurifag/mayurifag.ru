Vagrant.require_version ">= 2.2.2"

required_plugins = ["vagrant-hostmanager", "vagrant-cachier"]
required_plugins.each do |plugin|
  if !Vagrant.has_plugin?(plugin)
    system "echo Not installed required plugin: #{plugin} ..."
    system "vagrant plugin install #{plugin}"
  end
end

Vagrant.configure(2) do |config|
  # https://github.com/devopsgroup-io/vagrant-hostmanager/issues/102
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.vm.define "mayurifag-test" do
    config.vm.box = "geerlingguy/debian10"
    config.ssh.insert_key = false

    # vagrant-cachier
    config.cache.scope = :box

    # vagrant-hostmanager
    config.vm.network "private_network", ip: "192.168.56.12"
    config.vm.hostname = "mayurifag.local"
    config.hostmanager.aliases = %w[
      glances.mayurifag.local
      homer.mayurifag.local
      netdata.mayurifag.local
      nextcloud.mayurifag.local
      portainer.mayurifag.local
      seafile.mayurifag.local
      traefik.mayurifag.local
      wallabag.mayurifag.local
      dozzle.mayurifag.local
    ]

    config.vm.provision "ansible_local", run: "always", type: :ansible_local do |ansible|
      ansible.compatibility_mode = "2.0"
      ansible.install_mode = "pip"
      ansible.galaxy_role_file = "requirements.yml"
      ansible.inventory_path = "tests/inventories/integration_testing/inventory"
      ansible.playbook = "provisioning.yml"
      ansible.become = true
      # Run only needed tags
      # ansible.tags = "portainer"
      # ansible.raw_arguments = [
      #   "--extra-vars @tests/test.yml"
      # ]
    end
  end
end
