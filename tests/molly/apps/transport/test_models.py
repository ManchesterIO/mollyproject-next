import geojson
from mock import Mock
from shapely.geometry import Point, Polygon
import unittest2 as unittest

from molly.apps.transport.models import Locality, Stop, CallingPoint
from molly.apps.common.components import Source

class LocalityTest(unittest.TestCase):

    _TEST_POINT = Point(54, 2)
    _TEST_SLUG = "http://tch/locality/manchester"
    _TEST_PARENT_SLUG = "http://tch/locality/england"
    _DUMMY_DICT = {'mock': True}

    def test_locality_slug_in_serialised_dict(self):
        locality_dict = self._get_test_locality_dict()

        self.assertIn('slug', locality_dict)
        self.assertEqual(self._TEST_SLUG, locality_dict['slug'])

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

        locality_dict = locality._asdict()

        self.assertEquals(self._get_point_dict(test_polygon.centroid),
            locality_dict['geography_centroid'])

    def test_locality_parent_slug_in_serialised_dict(self):
        locality_dict = self._get_test_locality_dict()

        self.assertIn('parent_slug', locality_dict)
        self.assertEqual(self._TEST_PARENT_SLUG, locality_dict['parent_slug'])

    def test_sources_in_serialised_dict(self):
        locality = self._build_test_locality()
        locality.sources = [self._build_mock_serialisable()]

        locality_dict = locality._asdict()

        self.assertIn('sources', locality_dict)
        self.assertEqual([self._DUMMY_DICT], locality_dict['sources'])

    def test_identifiers_in_serialised_dict(self):
        locality = self._build_test_locality()
        locality.identifiers = [self._build_mock_serialisable()]

        locality_dict = locality._asdict()

        self.assertIn('identifiers', locality_dict)
        self.assertEqual([self._DUMMY_DICT], locality_dict['identifiers'])

    def _build_test_locality(self):
        locality = Locality()
        locality.geography = self._TEST_POINT
        locality.slug = self._TEST_SLUG
        locality.parent_slug = self._TEST_PARENT_SLUG
        return locality

    def _get_test_locality_dict(self):
        return self._build_test_locality()._asdict()

    def _get_point_dict(self, point):
        return geojson.GeoJSONEncoder().default(point)

    def _build_mock_serialisable(self):
        source = Mock()
        source._asdict = Mock()
        source._asdict.return_value = self._DUMMY_DICT
        return source


class StopTest(unittest.TestCase):

    def test_stop_as_dict_includes_appropriate_things(self):
        slug = '/test'
        source = Source(url='http://www.example.com', version=1, attribution=None)
        calling_point_slug = '/foo'

        stop = Stop()
        stop.slug = '/test'
        stop.sources.add(source)
        stop.calling_points.add(calling_point_slug)

        self.assertEquals({
            'slug': slug,
            'sources': [source._asdict()],
            'calling_points': [calling_point_slug],
            'identifiers': []
        }, stop._asdict())


class CallingPointTest(unittest.TestCase):

    def test_stop_as_dict_includes_appropriate_things(self):
        slug = '/test'
        source = Source(url='http://www.example.com', version=1, attribution=None)
        parent_slug = '/foo'

        calling_point = CallingPoint()
        calling_point.slug = '/test'
        calling_point.sources.add(source)
        calling_point.parent_slug = parent_slug

        self.assertEquals({
            'slug': slug,
            'sources': [source._asdict()],
            'parent_slug': parent_slug,
            'identifiers': []
        }, calling_point._asdict())

    def test_stop_as_dict_includes_appropriate_things_when_no_parent(self):
        slug = '/test'
        source = Source(url='http://www.example.com', version=1, attribution=None)

        calling_point = CallingPoint()
        calling_point.slug = '/test'
        calling_point.sources = [source]

        self.assertEquals({
            'slug': slug,
            'sources': [source._asdict()],
            'parent_slug': None,
            'identifiers': []
        }, calling_point._asdict())
