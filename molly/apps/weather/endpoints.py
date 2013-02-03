from flask import url_for
from molly.apps.common.endpoints import Endpoint

class ObservationsEndpoint(Endpoint):

    def __init__(self, instance_name, provider):
        self._provider = provider
        self._href = lambda: url_for(instance_name + '.observation', _external=True)

    def component(self):
        return {
            'self': 'http://mollyproject.org/apps/weather/observation',
            'href': self._href(),
            'observation': self._provider.latest_observations(),
            'attribution': self._provider.attribution._asdict()
        }

    def get(self):
        return self._json_response(self.component())
