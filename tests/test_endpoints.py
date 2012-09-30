import json
from mock import Mock
import unittest2 as unittest

from molly.apps.weather.endpoints import ObservationsEndpoint

class ObservationsEndpointTest(unittest.TestCase):

    _OBSERVATION = {'hello': 'world'}
    _ATTRIBUTION = {'attibution': 'Yes'}

    def setUp(self):
        self._provider = Mock()
        self._provider.latest_observations = Mock(return_value=self._OBSERVATION)
        self._provider.attribution = self._ATTRIBUTION
        self._endpoint = ObservationsEndpoint(self._provider)

    def test_observations_included_in_response(self):
        response = json.loads(self._endpoint.get().data)
        self.assertEquals(self._OBSERVATION, response['observation'])

    def test_attribution_included_in_response(self):
        response = json.loads(self._endpoint.get().data)
        self.assertEquals(self._ATTRIBUTION, response['attribution'])
