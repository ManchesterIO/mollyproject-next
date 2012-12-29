from flask.ext.script import Manager

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import unittest2 as unittest

from molly.config import ConfigLoader, ConfigError

from tests.test_providers.provider import Provider as TestProvider
from tests.test_services.service import Service as TestService

class ConfigLoaderTestCase(unittest.TestCase):

    def setUp(self):
        self._config_loader = ConfigLoader(None)

    def tearDown(self):
        SIMPLE_TEST_CONFIG.reset()
        PROVIDER_TEST_CONFIG.reset()

    def test_config_loader_returns_list_of_apps(self):
        config, apps, services = self._config_loader.load_from_config(StringIO(""))
        self.assertEquals(0, len(apps))

    def test_config_loader_loads_apps(self):
        config, apps, services = self._config_loader.load_from_config(SIMPLE_TEST_CONFIG)
        self.assertEquals('test', apps[0].instance_name)

    def test_config_loader_passes_config_dict_to_app(self):
        config, apps, services = self._config_loader.load_from_config(SIMPLE_TEST_CONFIG)
        self.assertEquals('bar', apps[0].config['foo'])

    def test_config_loader_creates_providers_for_app(self):
        config, apps, services = self._config_loader.load_from_config(PROVIDER_TEST_CONFIG)
        self.assertIsInstance(apps[0].providers[0], TestProvider)

    def test_config_loader_puts_config_into_provider(self):
        config, apps, services = self._config_loader.load_from_config(PROVIDER_TEST_CONFIG)
        self.assertEquals('baz', apps[0].providers[0].config['bar'])

    def test_config_loader_raises_config_exception_on_no_such_app(self):
        self.assertRaises(ConfigError, self._config_loader.load_from_config, BAD_APP_CONFIG)

    def test_config_loader_raises_config_exception_on_no_such_provider(self):
        self.assertRaises(ConfigError, self._config_loader.load_from_config, BAD_PROVIDER_CONFIG)

    def test_module_is_compulsory_field(self):
        self.assertRaises(ConfigError, self._config_loader.load_from_config, MISSING_APP_CONFIG)

    def test_provider_is_compulsory_field(self):
        self.assertRaises(ConfigError, self._config_loader.load_from_config, MISSING_PROVIDER_CONFIG)

    def test_services_are_passed_to_app(self):
        config, apps, services = self._config_loader.load_from_config(SERVICES_CONFIG)
        self.assertIsInstance(apps[0].services['test'], TestService)
        self.assertIsInstance(services['test'], TestService)

    def test_global_config_is_extracted(self):
        config, apps, services = self._config_loader.load_from_config(GLOBAL_CONFIG)
        self.assertEquals(True, config['DEBUG'])

    def test_default_cli_service_is_created(self):
        config, apps, services = self._config_loader.load_from_config(StringIO(""))
        self.assertIsInstance(services['cli'], Manager)


SIMPLE_TEST_CONFIG = StringIO("""
[test]
module = tests.test_apps.app
foo = bar
""")

PROVIDER_TEST_CONFIG = StringIO("""
[test]
module = tests.test_apps.app
foo = bar
provider.test = tests.test_providers.provider
provider.test.bar = baz
""")

BAD_APP_CONFIG = StringIO("""
[test]
module = does.not.exist
""")

BAD_PROVIDER_CONFIG = StringIO("""
[test]
module = tests.test_apps.app
provider.test = does.not.exist
""")

MISSING_APP_CONFIG = StringIO("""
[test]
foo = bar
""")

MISSING_PROVIDER_CONFIG = StringIO("""
[test]
module = tests.test_apps.app
provider.test.bar = baz
""")

SERVICES_CONFIG = StringIO("""
[test]
module = tests.test_apps.app

[services]
test = tests.test_services.service
""")

GLOBAL_CONFIG = StringIO("""
[global]
DEBUG = True
""")
