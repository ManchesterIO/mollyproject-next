from molly.apps.common.endpoints import Endpoint

class ObservationsEndpoint(Endpoint):

    def __init__(self, provider):
        self._provider = provider

    def get(self):
        return self._json_response({
            'observation': self._provider.latest_observations(),
            'attribution': self._provider.attribution
        })
