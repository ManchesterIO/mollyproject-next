from flask import Blueprint, url_for
from flaskext.babel import lazy_gettext as _

from molly.apps.weather.endpoints import ObservationsEndpoint

class App(object):

    module = 'http://mollyproject.org/apps/weather'

    def __init__(self, instance_name, config, providers=[]):
        self.instance_name = instance_name
        self._provider = providers.pop()

        self.human_name = _('Weather')

        self.blueprint = Blueprint(self.instance_name, __name__)
        self.blueprint.add_url_rule(
            '/', 'observation',
            ObservationsEndpoint(self.instance_name, self._provider).get
        )

    @property
    def links(self):
        return [self._provider.latest_observations()]
