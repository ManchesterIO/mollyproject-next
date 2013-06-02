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
* Run 'vagrant up' in the root
* Visit http://192.168.33.10:8000/ for the REST endpoints
* Visit http://192.168.33.10:8002/ for the prototype HTML5 frontend
* Populate some data: run 'vagrant ssh', then in the new shell 'cd /vagrant; PYTHONPATH=/vagrant /opt/molly/bin/mollyrest import_openstreetmap_places'

Running unit tests
------------------

(you'll be best doing development in a virtualenv)

* You'll need libgeos, protobufs and a compiler installed (Use brew on Mac or your favourite package manager)
* pip install -r requirements.txt
* python setup.py test

To run JavaScript unit tests, grab a copy of JSTestDriver and use the provided config file to run it (or use your
favourite IDE), e.g.,

java -jar JsTestDriver-1.3.3d.jar --reset --port 9874 --browser firefox --tests all --config JSTestDriver.jstd


Running behavioural tests
-------------------------

The behavioural tests are written using Cucumber and Ruby, so you need to have a Ruby runtime installed and phantomjs.
RVM is recommended and there's a .rvmrc file in here which should configure Ruby correctly if you're using RVM. To
install the dependencies, run 'bundle' in the root, and to run the tests themselves, execute 'bundle exec cucumber'.
