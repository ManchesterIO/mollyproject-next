from ConfigParser import ConfigParser
from collections import OrderedDict
from importlib import import_module
from flask.ext.script import Manager

class ConfigLoader(object):

    def __init__(self, flask_app):
        self._flask_app = flask_app

    def load_from_config(self, config):
        apps = []
        parser = ConfigParser()
        parser.readfp(config)

        if parser.has_section('services'):
            services = self._initialise_services(parser.items('services'))
        else:
            services = {}

        if services.get('cli', None) is None:
            services['cli'] = Manager(self._flask_app, with_default_commands=False)

        if parser.has_section('global'):
            global_config = dict((key.upper(), eval(value)) for (key, value) in parser.items('global'))
        else:
            global_config = {}

        for section in parser.sections():
            if section not in ('services', 'global'):
                apps.append(self._initialise_app(section, OrderedDict(parser.items(section)), services))

        return global_config, apps, services

    def _initialise_services(self, config):
        services = {}
        for service_name, service_package in config:
            if ':' in service_package:
                service_module, service_class = service_package.split(':')
            else:
                service_module, service_class = service_package, 'Service'
            services[service_name] = getattr(import_module(service_module), service_class)()
        return services

    def _initialise_app(self, name, config, services):
        providers = self._initialise_providers(config)
        module_name = config.get('module')
        if module_name is None:
            raise ConfigError('Module name not defined for app ' + name)
        try:
            app_module = import_module(module_name)
        except ImportError:
            raise ConfigError("Unable to find module: " + config['module'])
        return app_module.App(name, config, providers, services)

    def _initialise_providers(self, config):
        providers = []
        for module_name, config in self._get_provider_config(config):
            try:
                provider_module = import_module(module_name)
            except ImportError:
                raise ConfigError("Unable to find provider: " + module_name)
            providers.append(provider_module.Provider(config))
        return providers

    def _get_provider_config(self, config):
        configs = {}
        for key, value in config.items():
            key_parts = key.split('.', 3)
            if len(key_parts) == 2:
                configs[key_parts[1]] = (value, {})
            elif len(key_parts) == 3:
                if key_parts[1] not in configs:
                    raise ConfigError("Provider " + key_parts[1] + " module must be declared before configuring it")
                configs[key_parts[1]][1][key_parts[2]] = value
        return configs.values()


class ConfigError(Exception):
    pass
