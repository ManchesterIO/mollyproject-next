from mock import Mock
import unittest2

from molly.apps.places import models

class TestPointsOfInterest(unittest2.TestCase):

    def setUp(self):
        self._mock_mongo = Mock()
        self._pois = models.PointsOfInterest(self._mock_mongo)

    def test_add_adds_to_database(self):
        self._mock_mongo.pois.find_one.return_value = None
        poi = models.PointOfInterest()
        self._pois.add_or_update(poi)
        self._mock_mongo.pois.insert.assert_called_once_with(poi.as_dict())

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
