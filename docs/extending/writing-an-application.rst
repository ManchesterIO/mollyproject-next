Writing an Application
======================

Applications in Molly are components which plug into the framework and provide RESTful endpoints to the end users.

Applications live in packages and are loaded according to the configuration file. To define a minimal application,
you have to define a class called 'App' at the root of your package. :class:`molly.apps.common.app.BaseApp` provides
some common functionality that you might want to use.

Your App class should look like this:

.. class:: App(instance_name, config, providers, services)

    :param instance_name: This is the unique name identifying this instance of this app - it is used as the base URL
                          prefix which this app is exposed under
    :type instance_name: str
    :param config: A dictionary of config values specified in the config file
    :type config: dict
    :param providers: A list of instantiated providers for your app as defined in the config file
    :type providers: list
    :param services: A dictionary of objects which provide an advertised service
    :type services: dict

    Applications are instantiated with config read from the config file, a unique instance name, and any providers which
    are declared in the config file. Additionally, available to apps are a set of common services, for example caching
    or a key-value store. Objects which correspond to a defined interface are exposed under well-known names.

    .. attribute:: module

        :type: str
        This should be a URI uniquely identifying this module, e.g., http://mollyproject.org/apps/example

    .. attribute:: human_name

        :type: unicode
        This should be this should a human-readable name for the instance. As applications can be instantiated multiple
        times, you may find it useful to include some sort of disambiguator here. For example, if you are building a
        weather app, then you might want to include the name of the forecast area, so if multiple copies of the weather
        app are instantiated (for example, split-site campuses wanting to show weather forecasts for each campus)
        then it is clear which weather area is being shown.

    .. attribute:: instance_name

        :type: str
        This is the slug which identifies which instance of the app this is, in most circumstances this will be set to
        the value which is passed to the constructor

    .. attribute:: blueprint

        :type: :class:`flask.Blueprint`
        This is a `Flask blueprint <http://flask.pocoo.org/docs/blueprints/>`_ object which will be added to the
        deployed Flask app at a URL prefix of ``/instance_name``

    .. attribute:: links

        :type: list
        This should return a list of dictionaries which correspond to the components you wish to expose on the homepage
        for this app.