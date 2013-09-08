Configuring your Molly install
==============================

Your Molly install config file is a standard config file similar to .ini files found on Windows systems.

::

    [services]
    cache = flask.ext.cache:Cache
    i18n = flask.ext.babel:Babel
    kv = flask.ext.pymongo:PyMongo
    tasks = molly.services.tasks

    # To enable Sentry on this install, simply uncomment this and the SENTRY_DSN line below,
    # and add your DSN for Sentry to the config value
    #sentry = raven.contrib.flask:Sentry

    # To enable statsd on this install, simply uncomment this and the STATSD_HOST below
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

Services
--------

This area configures services which are available to all apps. Each service is specified under a well known name
and the value is in the form of ``module:class`` (if ``:class`` is omitted it defaults to :class:``Service``)

Global
------

Flask extensions do not support the instance specific configs of themselves, but are used as Molly services, and
expect global configuration values on the Flask object. This area of the config can be used to set those type of values.

Applications
------------

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