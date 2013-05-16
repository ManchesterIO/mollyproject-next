import json
from flask import Flask
from mock import Mock
import unittest2 as unittest

from werkzeug.exceptions import NotFound

from molly.apps.places.endpoints import PointOfInterestEndpoint
from molly.apps.places.models import PointOfInterest


class PointOfInterestEndpointTest(unittest.TestCase):

    def setUp(self):
        self._poi_service = Mock()
        self._endpoint = PointOfInterestEndpoint('testplaces', self._poi_service)

    def test_point_of_interest_returns_404_when_url_invalid(self):
        self._poi_service.select_by_slug.return_value = None
        self.assertRaises(NotFound, self._endpoint.get, 'foo:bar')

    def test_point_of_interest_returns_correct_self_when_url_valid(self):
        self._poi_service.select_by_slug.return_value = PointOfInterest()
        response = self._get_response_json()
        self.assertEquals('http://mollyproject.org/apps/places/point-of-interest', response['self'])

    def test_href_included_in_response(self):
        self._poi_service.select_by_slug.return_value = PointOfInterest()
        response = self._get_response_json()
        self.assertEquals('http://localhost/poi/foo:bar', response['href'])

    def test_poi_serialised_in_response(self):
        self._poi_service.select_by_slug.return_value = PointOfInterest(telephone_number='999')
        response = self._get_response_json()
        self.assertEquals('999', response['poi']['telephone_number'])

    def _get_response_json(self):
        app = Flask(__name__)
        app.add_url_rule('/poi/<slug>', 'testplaces.poi', self._endpoint.get)
        with app.test_request_context('/', headers=[('Accept', 'application/json')]):
            return json.loads(self._endpoint.get('foo:bar').data)