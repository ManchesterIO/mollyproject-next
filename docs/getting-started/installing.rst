Installing Molly
================

.. seealso:: :doc:`quick-start`

Molly is a web application framework that builds on top of a lot of other projects (we don't believe in reinventing the
wheel and do believe in the right tool for the job). As such, it has a bunch of other dependencies that need to be
installed first.

.. note:: You might see 'flask' mentioned a lot, Molly itself is built on the Flask micro-framework, and we can use a
          lot of the Flask ecosystem to make our job a lot easier.

Pre-requisites
--------------

Software Libraries
~~~~~~~~~~~~~~~~~~

.. note:: If you are using Chef, these will be automatically installed for you.

Molly requires the following software libraries to be installed on your system, they're frequently available using
a package manager on most platforms:

* Python 2.7
* Ruby
* `libgeos <http://trac.osgeo.org/geos/>`_ (Ubuntu: ``libgeos-c1``)
* `protobuf <https://code.google.com/p/protobuf/>`_ (Ubuntu: ``llibprotobuf-dev`` and ``protobuf-compiler``)

Additionally the following Ruby Gems need to be installed, this can be done by using the ``gem`` command:

* compass
* zurb-foundation

Services
~~~~~~~~

Molly uses a number of external services in order to provide things such as data persistence which must be made available
to Molly. These services are:

* `ElasticSearch <http://www.elasticsearch.org/>`_
* `Memcached <http://memcached.org/>`_
* `MongoDB <http://www.mongodb.org/>`_
* `RabbitMQ <http://www.rabbitmq.com/>`_

.. note:: Flask-Cache supports a number of caching services out of the box, including a null cache, so it is possible to
          use caches other than memcached, but memcached is the only supported configuration.

.. todo:: Better configuration, at the moment, Molly just connects to those services using default settings

Using Chef
----------

If you're using Chef, then your job has just become a lot easier! The Molly Project uses Chef internally for our own
deployments, so we maintain `a cookbook for Molly <https://github.com/ManchesterIO/cookbook-molly>`_ to ease deployment.

Simply import the cookbook and then add the following recipes:

* ``mollyproject::install_git_master`` to install Molly from the latest version in GitHub
* ``mollyproject`` to configure the installed version

.. todo:: Add PyPI recipe when we are closer to release

You can configure the install of Molly by using the following settings in your node attributes::

    {
        "mollyproject": {
            "user": "molly", # The user molly runs as on the deployed machine
            "sandbox": false, # Whether or not this install should be from the sandbox (i.e., one where code can be edited from the host machine)
            "debug": false, # Whether or not debug mode is enabled, this causes detailed error messages to be displayed
            "bind_all": false, # Whether or not to bind to external IPs, highly discouraged in production
            "install_root": "/opt/molly", # where Molly is installed to
            "config": "/opt/molly/conf/default.conf", # where Molly should find the config file for the REST server
            "ui": {
                "settings": "/opt/molly/conf/ui.py", # where Molly should find the config file for the UI server
                "module": "molly.ui.html5.server:flask_app" # which module Molly should use to run the UI server
            }
        }
    }

Please note that this does not configure any external services which Molly depends on. The dependent services listed above
must be available for Molly to behave correctly.

.. note:: Handily, all these services have Chef cookbooks.

The Chef cookbook will configure the Molly REST, UI and tasks servers to automatically start and uses supervisor to
control these.

Manual Install
--------------

Molly is designed to make automated deploys as pain-free as possible, but at present, only comes with pre-built scripts
for Chef. If you want to deploy Molly by hand, or automate it with your own tool set, these are the instructions to follow.

How you structure your server is best for you to decide, but we highly recommend running Molly as its own user on your
server and using virtualenv as documented below. The following actions assume you are running as the user you want to
run molly as.

Virtualenv
~~~~~~~~~~

A standard Python tool called ``virtualenv`` can be used to isolate a Python application and its dependencies from the
system. Using a virtualenv for Molly is highly recommended. The rest of this guide assumes that you have created a
virtualenv in ``/opt/molly`` but you are not required to (just replace ``/opt/molly`` with your own path in the rest
of the guide if you wish).

To create a virtualenv, you can run the following commands::

    pip install virtualenv
    virtualenv /opt/molly

Installing Molly
~~~~~~~~~~~~~~~~

Now your machine is all set up, all we need to do is drop the Molly code on it

### From PyPI

.. todo:: Molly-next will not appear on PyPI until it is closer to release

### From GitHub

::

    /opt/molly/bin/pip install git+https://github.com/ManchesterIO/mollyproject-next.git

### From local download

From a local checkout of Molly, run::

    /opt/molly/bin/python /path/to/molly/setup.py install


Sentry and Statsd (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Molly also comes with out of the box support for `Statsd <https://github.com/etsy/statsd/>`_ (performance metric analysis)
and `Sentry <https://getsentry.com/>`_ (error logging), but does not require these to be installed. In order to add this
functionality to Molly, you can simply install the optional dependencies using ``pip`` and enable them in
:doc:`the config file <configuring>`::

    /opt/molly/bin/pip install Flask-StatsD
    /opt/molly/bin/pip install raven[flask]
