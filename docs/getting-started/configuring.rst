Configuring your Molly install
==============================

Config File format
------------------

Your Molly install config file is a standard config file similar to .ini files found on Windows systems.

::

    [services]
    cache = flask.ext.cache:Cache
    i18n = flask.ext.babel:Babel
    kv = flask.ext.pymongo:PyMongo
    tasks = molly.services.tasks
    #sentry = raven.contrib.flask:Sentry
    #statsd = flask.ext.statsd:StatsD

    [global]
    CACHE_TYPE = "memcached"
    SOLR_URL = "http://localhost:8080/solr"
    #SENTRY_DSN = ""
    #STATSD_HOST = "localhost"

    [places]
    module = molly.apps.places
    provider.openstreetmap = molly.apps.places.importers.openstreetmap
    provider.openstreetmap.url = http://osm-extracted-metros.s3.amazonaws.com/manchester.osm.pbf
    provider.naptan = molly.apps.places.importers.naptan

    [weather]
    module = molly.apps.weather
    provider.metoffice = molly.apps.weather.providers.metoffice
    provider.metoffice.api_key = 123456-456789
    provider.metoffice.location_id = 3330

The config file is structured with 2 required sections called ``services`` and ``global``, followed by a section for
each application enabled on this install. Lines starting with the ``#`` symbol are ignored.

``[services]``
--------------

This area configures services which are available to all apps. Each service is specified by giving a name of the service
which applications expect to find (e.g., ``kv`` for the KV store, ``cache`` for a caching service, etc)
and the value is in the form of ``module:class`` (if ``:class`` is omitted it defaults to :class:``Service``)

In order to simplify things, services are opinionated, and expect to implement a particular interface which may be
heavily coupled to a particular server type. For example, the ``kv`` service is expected to be MongoDB.

.. seealso: :doc:`../extending/writing-a-service`

.. todo:: Ship with default service configuration, only override if need be. Services need configuring way better.

``[global]``
------------

There are some settings which apply to the entire server, rather than just a single app installed on it. This includes
most of the service configuration.

.. todo:: List important settings and link to full list for interested parties.

Applications
------------

.. todo:: Explain this better and include lots of examples

Applications are specified in the form::

    [INSTANCE_NAME]
    module = MODULE_PATH
    option1 = value1
    ...

Providers
.........

If an application supports providers, you can specify them by adding a key in the form: ``provider.NAME = MODULE``.
If the provider takes any more configuration options, they can be added by having config values in the form:
``provider.NAME.OPTION = VALUE``

UI Config
---------

.. todo:: All of this