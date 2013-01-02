from mock import Mock
from shapely.geometry import Point
import unittest2

from molly.apps.common.components import LocalisedName
from molly.apps.places import models

class TestPointsOfInterest(unittest2.TestCase):

    def setUp(self):
        self._mock_mongo = Mock()
        self._mock_solr = Mock()
        self._pois = models.PointsOfInterest('test', self._mock_mongo, self._mock_solr)
        self._mock_mongo.pois.find_one.return_value = None

    def test_add_adds_to_database(self):
        poi = models.PointOfInterest()
        self._pois.add_or_update(poi)
        self._mock_mongo.pois.insert.assert_called_once_with(poi.as_dict())

    def test_add_indexes(self):
        poi = models.PointOfInterest()
        poi.uri = '/osm:N12345'
        poi.names = [LocalisedName(name='Test', lang='en')]
        poi.descriptions = [LocalisedName(name='Descriptions', lang='en')]
        poi.geography = Point(-1.6, 54.0)
        poi.identifiers = [models.Identifier(namespace='foo', value='bar')]

        self._pois.add_or_update(poi)
        self._mock_solr.add.assert_called_once_with({
            'id': '/test/osm:N12345',
            'self': 'http://mollyproject.org/apps/places/point-of-interest',
            'names': ['Test'],
            'descriptions': ['Descriptions'],
            'identifiers': ['bar'],
            'location': '54.0,-1.6'
        })

    def test_add_or_update_checks_for_uri_clashes_before_adding(self):
        self._mock_mongo.pois.find_one.return_value = {
            '_id': 'abcdef', 'sources': [models.Source(url='http://www.example.com', version=1, attribution='OSM')]
        }
        poi = models.PointOfInterest(uri='/test:test')
        self._pois.add_or_update(poi)
        poi_dict = poi.as_dict()
        poi_dict.update({'_id': 'abcdef'})
        self.assertFalse(self._mock_mongo.pois.insert.called)
        self._mock_mongo.pois.update.assert_called_once_with(poi_dict)

    def test_add_or_update_does_not_update_if_source_has_not_changed(self):
        self._mock_mongo.pois.find_one.return_value = {
            '_id': 'abcdef',
            'sources': [{'url': 'http://www.example.com', 'version': 1, 'attribution': 'OSM'}]
        }

        poi = models.PointOfInterest(
            uri='/test:test', sources=[models.Source(url='http://www.example.com', version=1, attribution='OSM')]
        )
        self._pois.add_or_update(poi)

        self.assertFalse(self._mock_mongo.pois.insert.called)
        self.assertFalse(self._mock_mongo.pois.update.called)
        self.assertFalse(self._mock_solr.add.called)
