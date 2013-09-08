``kv`` - key-value store
========================

.. note:: This service is opinionated in that it exposes MongoDB directly, rather than providing an abstraction to a
          more general case KV store.

This service provides an interface to a key-value store.
This is `Flask-PyMongo <http://flask-pymongo.readthedocs.org/en/latest/>`_.