Molly 2.0
=========

This is a early code for a proposed Molly 2.0 architecture.

Discussion is encouraged on the mollyproject-devel list. This is by no means the final shape of Molly 2.0.

Running Molly
-------------

* Make sure Vagrant is installed
* Run 'vagrant up' in the root
* Visit http://192.168.33.10:8000/ for the REST endpoints
* Visit http://192.168.33.10:8002/ for the prototype HTML5 frontend

Running unit tests
------------------

* python setup.py test

This is quite far from having feature parity with 1.4 and requires a minimum of Python 2.7

[![Build Status](https://api.travis-ci.org/mollyproject/mollyproject.png?branch=molly2)](https://travis-ci.org/mollyproject/mollyproject)