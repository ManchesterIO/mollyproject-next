# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :hostonly, "192.168.33.10"

  config.vm.forward_port 80, 8000
  config.vm.forward_port 8002, 8002

  config.vm.provision :chef_solo do | chef |
    chef.add_recipe "mongodb::10gen_repo"
    chef.add_recipe "memcached"
    chef.add_recipe "python"
    chef.add_recipe "mongodb::default"
    chef.add_recipe "molly::develop"
  end

end
