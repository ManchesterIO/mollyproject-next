``statsd`` - Monitoring and Metrics
===================================

.. note:: This service is opinionated and was designed with statsd in mind.

This service exposes a simple statsd-like interface for metric collection. It is `Flask-StatsD <https://github.com/cyberdelia/flask-statsd>`_.

You can always assume this service is here - if it is not configured, then a no-op version with the same interface
is put in its place.