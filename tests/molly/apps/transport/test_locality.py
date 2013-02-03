import geojson
from mock import Mock
from shapely.geometry import Point, Polygon
import unittest2 as unittest

from molly.apps.transport.locality import Locality

class LocalityTest(unittest.TestCase):

    _TEST_POINT = Point(54, 2)
    _TEST_URL = "http://tch/locality/manchester"
    _TEST_PARENT_URL = "http://tch/locality/england"
    _DUMMY_DICT = {'mock': True}

    def test_locality_url_in_serialised_dict(self):
        locality_dict = self._get_test_locality_dict()

        self.assertIn('url', locality_dict)
        self.assertEqual(self._TEST_URL, locality_dict['url'])

    def test_locality_geometry_in_serialised_dict(self):
        locality_dict = self._get_test_locality_dict()

        self.assertIn('geography', locality_dict)
        self.assertEquals(self._get_point_dict(self._TEST_POINT),
            locality_dict['geography'])

    def test_locality_centre_in_serialised_dict(self):
        locality_dict = self._get_test_locality_dict()

        self.assertIn('geography_centroid', locality_dict)
        self.assertEquals(self._get_point_dict(self._TEST_POINT),
            locality_dict['geography_centroid'])

    def test_locality_centre_in_serialised_dict_from_polygon(self):
        locality = self._build_test_locality()
        test_polygon = Polygon([(54, 2), (55, 2), (55, 3)])
        locality.geography = test_polygon

        locality_dict = locality.as_dict()

        self.assertEquals(self._get_point_dict(test_polygon.centroid),
            locality_dict['geography_centroid'])

    def test_locality_parent_url_in_serialised_dict(self):
        locality_dict = self._get_test_locality_dict()

        self.assertIn('parent_url', locality_dict)
        self.assertEqual(self._TEST_PARENT_URL, locality_dict['parent_url'])

    def test_sources_in_serialised_dict(self):
        locality = self._build_test_locality()
        locality.sources = [self._build_mock_serialisable()]

        locality_dict = locality.as_dict()

        self.assertIn('sources', locality_dict)
        self.assertEqual([self._DUMMY_DICT], locality_dict['sources'])

    def test_identifiers_in_serialised_dict(self):
        locality = self._build_test_locality()
        locality.identifiers = [self._build_mock_serialisable()]

        locality_dict = locality.as_dict()

        self.assertIn('identifiers', locality_dict)
        self.assertEqual([self._DUMMY_DICT], locality_dict['identifiers'])

    def _build_test_locality(self):
        locality = Locality()
        locality.geography = self._TEST_POINT
        locality.url = self._TEST_URL
        locality.parent_url = self._TEST_PARENT_URL
        return locality

    def _get_test_locality_dict(self):
        return self._build_test_locality().as_dict()

    def _get_point_dict(self, point):
        return geojson.GeoJSONEncoder().default(point)

    def _build_mock_serialisable(self):
        source = Mock()
        source.as_dict = Mock()
        source.as_dict.return_value = self._DUMMY_DICT
        return source
