# coding=utf-8
from flask import Flask
from mock import Mock
from requests.exceptions import RequestException
from shapely.geometry import Point
import unittest2 as unittest
from werkzeug.contrib.cache import NullCache

from molly.ui.html5.filters.geocoding import requests, reverse_geocode
from molly.services.stats import NullStats


class ReverseGeocodeTestCase(unittest.TestCase):
    _API_KEY = 'bcdefg'

    def setUp(self):
        self._flask = Flask(__name__)
        self._flask.config['CLOUDMADE_API_KEY'] = self._API_KEY
        self._flask.statsd = NullStats()
        self._flask.cache = NullCache()
        requests.get = Mock()

    def test_request_is_made_to_cloudmade(self):
        requests.get.return_value.json.return_value = {}
        with self._flask.test_request_context():
            reverse_geocode(Point(-10.0, 16.8))
        requests.get.assert_called_once_with(
            'http://beta.geocoding.cloudmade.com/v3/{key}/api/geo.location.search.2'.format(
                key=self._API_KEY
            ) + '?format=json&source=OSM&q=[latitude=16.8];[longitude=-10.0]'
        )

    def test_lat_lon_returned_when_success_false(self):
        requests.get.return_value.json.return_value = {
            "status": {
                "duration": 53, "message": "Search failed: no or too many results found",
                "procedure": "geo.location.search.2", "reason": "failed", "success": False
            }
        }
        self._expect_fallback_response()

    def test_lat_lon_returned_when_invalid_response(self):
        requests.get.return_value.json.side_effect = ValueError()
        self._expect_fallback_response()

    def test_lat_lon_returned_when_connection_fails(self):
        requests.get.side_effect = RequestException()
        self._expect_fallback_response()

    def test_name_returned_when_found(self):
        requests.get.return_value.json.return_value = {
            "places": [
                {"city": "~Manchester", "country": "United Kingdom", "name": "University of Manchester - Main Campus",
                 "position": {"lat": 53.45999996, "lon": -2.23000006}, "state": "England", "street": "Denmark Road"}],
            "status": {"duration": 21, "procedure": "geo.location.search.2", "success": True}
        }
        with self._flask.test_request_context():
            self.assertEquals('University of Manchester - Main Campus', reverse_geocode(Point(-10.0, 16.8)))

    def test_street_returned_when_no_name(self):
        requests.get.return_value.json.return_value = {
            "places": [
                {"city": "~Manchester", "country": "United Kingdom",
                 "position": {"lat": 53.45999996, "lon": -2.23000006}, "state": "England", "street": "Denmark Road"}],
            "status": {"duration": 21, "procedure": "geo.location.search.2", "success": True}
        }
        with self._flask.test_request_context():
            self.assertEquals('Denmark Road', reverse_geocode(Point(-10.0, 16.8)))

    def test_district_returned_when_no_street(self):
        requests.get.return_value.json.return_value = {
            "places": [
                {"city": "~Manchester", "country": "United Kingdom", "district": "Ancoats",
                 "position": {"lat": 53.45999996, "lon": -2.23000006}, "state": "England"}],
            "status": {"duration": 21, "procedure": "geo.location.search.2", "success": True}
        }
        with self._flask.test_request_context():
            self.assertEquals('Ancoats', reverse_geocode(Point(-10.0, 16.8)))

    def test_city_returned_when_no_district(self):
        requests.get.return_value.json.return_value = {
            "places": [
                {"city": "~Manchester", "country": "United Kingdom",
                 "position": {"lat": 53.45999996, "lon": -2.23000006}, "state": "England"}],
            "status": {"duration": 21, "procedure": "geo.location.search.2", "success": True}
        }
        with self._flask.test_request_context():
            self.assertEquals('Manchester', reverse_geocode(Point(-10.0, 16.8)))

    def test_lat_lon_returned_when_no_city(self):
        requests.get.return_value.json.return_value = {
            "places": [
                {"country": "United Kingdom", "position": {"lat": 53.45999996, "lon": -2.23000006}, "state": "England"}
            ],
            "status": {"duration": 21, "procedure": "geo.location.search.2", "success": True}
        }
        self._expect_fallback_response()

    def _expect_fallback_response(self):
        with self._flask.test_request_context():
            self.assertEquals(u'16.8˚, -10.0˚', reverse_geocode(Point(-10.0, 16.8)))
