import json
import urllib2
from flask import Flask
from mock import Mock, ANY, MagicMock
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
        self._poi_service.count_nearby_amenity = Mock(return_value=0)
        self._poi_service.count_nearby_category = Mock(return_value=0)
        self.maxDiff = None
        self._endpoint = NearbySearchEndpoint('testplaces', self._poi_service)
        self._endpoint.INTERESTING_CATEGORIES = {
            'test': 'http://example.com/testcat',
            'test2': 'http://example.com/testcat2'
        }
        self._endpoint.INTERESTING_AMENITIES = {
            'testamen': 'http://example.com/testamen',
        }
        self._endpoint.SEARCH_RADIUS = 123

    def _make_request(self, lat, lon):
        app = Flask(__name__)
        app.add_url_rule('/nearby/<float:lat>,<float:lon>', 'testplaces.nearby', self._endpoint.get)
        app.add_url_rule('/nearby/<float:lat>,<float:lon>/category/<slug>', 'testplaces.nearby_category', None)
        app.add_url_rule('/nearby/<float:lat>,<float:lon>/amenity/<slug>', 'testplaces.nearby_amenity', None)
        app.add_url_rule('/poi/<slug>', 'testplaces.poi', None)
        with app.test_request_context('/', headers=[('Accept', 'application/json')]):
            response = self._endpoint.get(lat, lon)
        return response

    def test_overly_precise_requests_are_rounded_down(self):
        response = self._make_request(10.123456789, 15.987654321)
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            'http://localhost/nearby/10.12346,15.98765',
            urllib2.unquote(dict(response.headers).get('Location'))
        )

    def test_search_results_are_in_correct_format(self):
        self._poi_service.search_nearby.return_value = []
        response = self._make_request(54.5, 0.6)
        self.assertEqual({
            'self': 'http://mollyproject.org/apps/places/categories',
            'categories': [],
            'amenities': []
        }, json.loads(response.data))

    def test_interesting_pois_are_searched_against(self):
        self._make_request(54.5, 0.6)

        self._poi_service.count_nearby_category.assert_any_call(ANY, 'http://example.com/testcat', radius=123)
        self._poi_service.count_nearby_category.assert_any_call(ANY, 'http://example.com/testcat2', radius=123)
        self._poi_service.count_nearby_amenity.assert_any_call(ANY, 'http://example.com/testamen', radius=123)

        point = self._poi_service.count_nearby_category.call_args[0][0]
        self.assertEqual((0.6, 54.5), (point.x, point.y))

        point = self._poi_service.count_nearby_amenity.call_args[0][0]
        self.assertEqual((0.6, 54.5), (point.x, point.y))

    def test_result_lists_are_in_correct_form(self):
        self._poi_service.count_nearby_category = Mock(side_effect=[3, 2])
        self._poi_service.count_nearby_amenity = Mock(return_value=6)
        response = json.loads(self._make_request(12.3, 6.8).data)
        self.assertEqual({
            'self': 'http://mollyproject.org/apps/places/categories',
            'categories': [{
                'self': 'http://mollyproject.org/apps/places/points-of-interest/by-category',
                'href': 'http://localhost/nearby/12.3%2C6.8/category/test',
                'category': 'http://example.com/testcat',
                'count': 3,
                'within': 123
            }, {
                'self': 'http://mollyproject.org/apps/places/points-of-interest/by-category',
                'href': 'http://localhost/nearby/12.3%2C6.8/category/test2',
                'category': 'http://example.com/testcat2',
                'count': 2,
                'within': 123
            }],
            'amenities': [{
                'self': 'http://mollyproject.org/apps/places/points-of-interest/by-amenity',
                'href': 'http://localhost/nearby/12.3%2C6.8/amenity/testamen',
                'amenity': 'http://example.com/testamen',
                'count': 6,
                'within': 123
            }]
        }, response)
