Molly 2.0 Responsive HTML5 proof-of-concept
===========================================

This is	a prototype proof-of-concept for a UI on the proposed Molly 2.0 architecture.

Discussion is encouraged on the mollyproject-devel list. This is by no means the final shape of Molly 2.0.

To get this running:

* Create a virtualenv (or re-use the Molly 2.0 core one)
* pip install -r requirements.txt
* python setup.py develop
* Start the molly2-core REST API on port 8000 (the default)
* Run: gunicorn --debug -b localhost:8002 molly
* Visit http://localhost:8002/

Run unit tests:

* python setup.py test

This is very, very alpha.

