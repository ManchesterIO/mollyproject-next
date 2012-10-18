Molly 2.0 REST proof-of-concept
===============================

This is a prototype proof-of-concept for a proposed Molly 2.0 architecture.

Discussion is encouraged on the mollyproject-devel list. This is by no means the final shape of Molly 2.0.

To get this running:

* Create a virtualenv
* pip install -r requirements.txt
* python setup.py develop
* Install molly2-weather inside the same virtualenv
* Customise conf/default.conf to your liking
* Run: gunicorn molly.rest:flask_app
* Visit http://localhost:8000, or alternatively start the UI project up

Run unit tests:

* python setup.py test

This is very, very alpha.
