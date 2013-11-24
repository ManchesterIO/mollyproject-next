Developer's Quick Start
=======================

Out of the box, Molly comes with a Vagrant sandbox to allow you to quickly get up to speed and experiment.

Vagrant is a tool for managing virtual machine configurations and also hooks in to provisioning systems such as Puppet
and Chef for deploying servers. Molly has been written with automated deployment tools in mind to make both
development and production deployments as similar as possible.

To get started with this sandbox, you need to have `VirtualBox <https://www.virtualbox.org/>`_ and
`Vagrant <http://www.vagrantup.com/>`_ installed. Once you have these tools installed, then you can simply grab a
copy of `the Molly codebase from GitHub <https://github.com/ManchesterIO/mollyproject-next>`_ and open a command line
in the ``sandbox`` folder of the checkout.

From within there, you should have access to the ``vagrant`` command. You must first install the Berkshelf plugin for
Vagrant: ``vagrant plugin install vagrant-berkshelf`` and then type ``vagrant up`` to start the Molly sandbox.

.. note:: On the first start of a new sandbox, many dependencies have to be downloaded. A fast Internet connection is
          recommended and it may take some time for the process to complete.

.. warning:: In some circumstances, rabbitmq will not start on the first boot. If the ``vagrant up`` command fails, then
          running ``vagrant reload --provision`` should reboot the virtual machine and complete the installation.

Once your sandbox is up and running, you should be able to access the API endpoints at http://192.168.33.10:8000/
and the UI at http://192.168.33.10:8002/.

The setup of Molly in the sandbox is such that making changes on your local machine should be reflected immediately in
the sandbox environment, however this is not perfect. The command ``vagrant reload --provision`` should reinstall Molly
on to the sandbox should that be needed.

To populate data into the sandbox you can run the following commands::

    vagrant ssh
    sudo -u molly env PYTHON_EGG_CACHE=/tmp MOLLY_CONFIG=/vagrant/conf/default.conf /opt/molly/bin/mollyrest import_naptan_places
    sudo -u molly env PYTHON_EGG_CACHE=/tmp MOLLY_CONFIG=/vagrant/conf/default.conf /opt/molly/bin/mollyrest import_openstreetmap_places

.. todo:: This should be improved so tasks which have never run before are automatically run on first-start
.. todo:: This should be improved so you don't need all the env vars

To close down the sandbox, run ``vagrant halt``. ``vagrant up`` can be used to start the sandbox again. To remove the
sandbox from your VirtualBox install then run ``vagrant destroy``.