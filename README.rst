Molly-next
==========

.. image:: https://secure.travis-ci.org/ManchesterIO/mollyproject-next.png
    :target: http://travis-ci.org/ManchesterIO/mollyproject-next
    :alt: Build Status

This is the framework for Manchester.IO inspired by the Molly Project 1.x framework to be a reusable framework between
cities and institutions. It is a suggested candidate for the Molly Project 2.x codebase, but will be developed
independently if that candidacy fails (probably under a new name).

This is quite far from having feature parity with Molly 1.4 and requires a minimum of Python 2.7

Running Molly
-------------

* Make sure Vagrant is installed
* Install the Berkshelf plugin for Vagrant: vagrant plugin install vagrant-berkshelf
* Run 'vagrant up' in the root
* Visit http://192.168.33.10:8000/ for the REST endpoints
* Visit http://192.168.33.10:8002/ for the prototype HTML5 frontend
* Populate some data: run 'vagrant ssh', then in the new shell 'cd /vagrant; PYTHONPATH=/vagrant /opt/molly/bin/mollyrest import_openstreetmap_places'

Running unit tests
------------------

(you'll be best doing development in a virtualenv)

* You'll need libgeos, protobufs and a compiler installed (Use brew on Mac or your favourite package manager)
* python setup.py test

To run JavaScript unit tests, you can open the 'tests/molly/ui/html5/js/TestRunner.html' in your browser or run
them using PhantomJS 'phantomjs tests/molly/ui/html5/js/runner.js'.
