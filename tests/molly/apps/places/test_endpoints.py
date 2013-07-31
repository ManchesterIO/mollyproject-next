import json
import urllib2
from flask import Flask
from mock import Mock
from shapely.geometry import Point
import unittest2 as unittest

from werkzeug.exceptions import NotFound

from molly.apps.places.endpoints import PointOfInterestEndpoint, NearbySearchEndpoint
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


class NearbySearchEndpointTest(unittest.TestCase):

    def setUp(self):
        self._poi_service = Mock()
        self.maxDiff = None

    def _make_request(self, lat, lon):
        endpoint = NearbySearchEndpoint('testplaces', self._poi_service)
        app = Flask(__name__)
        app.add_url_rule('/nearby/<float:lat>,<float:lon>', 'testplaces.nearby', endpoint.get)
        app.add_url_rule('/poi/<slug>', 'testplaces.poi', None)
        with app.test_request_context('/', headers=[('Accept', 'application/json')]):
            response = endpoint.get(lat, lon)
        return response

    def test_overly_precise_requests_are_rounded_down(self):
        response = self._make_request(10.123456789, 15.987654321)
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            'http://localhost/nearby/10.12346,15.98765',
            urllib2.unquote(dict(response.headers).get('Location'))
        )

    def test_search_is_passed_to_service(self):
        self._poi_service.search_nearby.return_value = []
        response = self._make_request(54.5, 0.6)
        self.assertEqual({
            'self': 'http://mollyproject.org/apps/places/points-of-interest',
            'points_of_interest': []
        }, json.loads(response.data))
        point = self._poi_service.search_nearby.call_args[0][0]
        self.assertEqual((0.6, 54.5), (point.x, point.y))

    def test_search_results_are_correctly_serialised(self):
        self._poi_service.search_nearby.return_value = [
            PointOfInterest(slug='foo:bar', telephone_number='01818118181')
        ]
        response = json.loads(self._make_request(54.5, 0.6).data)
        self.assertEqual('http://localhost/poi/foo:bar', response['points_of_interest'][0]['href'])
        self.assertEqual('01818118181', response['points_of_interest'][0]['telephone_number'])
