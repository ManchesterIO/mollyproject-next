import json
from flask import Flask
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
        self._endpoint = ObservationsEndpoint('weather', self._provider)

    def test_observations_included_in_response(self):
        response = self._get_response_json()
        self.assertEquals(self._OBSERVATION, response['observation'])

    def test_attribution_included_in_response(self):
        response = self._get_response_json()
        self.assertEquals(self._ATTRIBUTION, response['attribution'])

    def test_self_included_in_response(self):
        response = self._get_response_json()
        self.assertEquals('http://mollyproject.org/apps/weather/observation', response['self'])

    def test_href_included_in_response(self):
        response = self._get_response_json()
        self.assertEquals('http://localhost/weatherobs', response['href'])

    def _get_response_json(self):
        app = Flask(__name__)
        app.add_url_rule('/weatherobs', 'weather.observation', self._endpoint.get)
        with app.test_request_context('/', headers=[('Accept', 'application/json')]):
            return json.loads(self._endpoint.get().data)
