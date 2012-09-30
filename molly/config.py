from ConfigParser import ConfigParser
from importlib import import_module

class ConfigLoader(object):

    def __init__(self, app):
        self._flask_app = app

    def load_from_config(self, config):
        apps = []
        parser = ConfigParser()
        parser.readfp(config)
        for section in parser.sections():
            apps.append(self._initialise_app(section, dict(parser.items(section))))
        return apps

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

    def _initialise_app(self, name, config):
        providers = self._initialise_providers(config)
        module_name = config.get('module')
        if module_name is None:
            raise ConfigError('Module name not defined for app ' + name)
        try:
            app_module = import_module(module_name)
        except ImportError:
            raise ConfigError("Unable to find module: " + config['module'])
        return app_module.App(self._flask_app, name, config, providers)


class ConfigError(Exception):
    pass
