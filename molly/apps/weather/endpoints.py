import json

from flask import Response

class ObservationsEndpoint(object):

    def __init__(self, provider):
        self._provider = provider

    def get(self):
        response = Response()
        response.data = json.dumps({
            'observation': self._provider.latest_observations(),
            'attribution': self._provider.attribution
        }, default=unicode)
        return response
