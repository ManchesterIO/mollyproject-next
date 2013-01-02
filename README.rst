Molly 2.0
=========

.. image:: https://secure.travis-ci.org/mollyproject/mollyproject.png?branch=molly2
    :target: http://travis-ci.org/mollyproject/mollyproject
    :alt: Build Status

This is early code for a proposed Molly 2.0 architecture.

Discussion is encouraged on the mollyproject-devel list. This is by no means the final shape of Molly 2.0.

Running Molly
-------------

* Make sure Vagrant is installed
* Run 'vagrant up' in the root
* Visit http://192.168.33.10:8000/ for the REST endpoints
* Visit http://192.168.33.10:8002/ for the prototype HTML5 frontend

Running unit tests
------------------

(you'll be best doing development in a virtualenv)

* You'll need libgeos, protobufs and a compiler installed (Use brew on Mac or your favourite package manager)
* pip install -r requirements.txt
* python setup.py test

This is quite far from having feature parity with 1.4 and requires a minimum of Python 2.7
