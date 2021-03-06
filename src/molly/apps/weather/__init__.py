from flask import Blueprint
from flask.ext.babel import lazy_gettext as _
from werkzeug.contrib.cache import NullCache

from molly.apps.weather.endpoints import ObservationsEndpoint
from molly.services.stats import NullStats


class App(object):

    module = 'http://mollyproject.org/apps/weather'
    human_name = _('Weather')

    def __init__(self, instance_name, config, providers, services):
        self.instance_name = instance_name
        self._provider = providers.pop()
        self._provider.cache = services.get('cache', NullCache())
        self._provider.statsd = services.get('statsd', NullStats())

        self._observations_endpoint = ObservationsEndpoint(self.instance_name, self._provider)

        self.blueprint = Blueprint(self.instance_name, __name__)
        self.blueprint.add_url_rule('/', 'observation', self._observations_endpoint.get)

    @property
    def links(self):
        return [self._observations_endpoint.component()]
