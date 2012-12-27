from mock import Mock, MagicMock
from shapely.geometry import Polygon, LineString, Point
import unittest2

from molly.apps.places.importers import openstreetmap

class TestOpenStreetMapImporter(unittest2.TestCase):

    def setUp(self):
        openstreetmap.OSMParser = Mock()
        openstreetmap.OSMParser.return_value = Mock()
        openstreetmap.NamedTemporaryFile = Mock()
        openstreetmap.NamedTemporaryFile.return_value = MagicMock()
        openstreetmap.urlopen = Mock()
        self._osm_importer = openstreetmap.OpenStreetMapImporter()

    def test_imposm_configured_with_correct_attributes(self):
        openstreetmap.OSMParser.assert_called_once_with(
            coords_callback=self._osm_importer.handle_coords,
            nodes_callback=self._osm_importer.handle_nodes,
            ways_callback=self._osm_importer.handle_ways,
            nodes_tag_filter=self._osm_importer.filter_tags,
            ways_tag_filter=self._osm_importer.filter_tags,
        )

    def test_imposm_parses_against_temporary_file(self):
        temporary_file = openstreetmap.NamedTemporaryFile.return_value.__enter__.return_value
        temporary_file.name = '/tmp/foo'

        self._osm_importer.load('http://www.example.com')

        openstreetmap.OSMParser.return_value.parse.assert_called_once_with(temporary_file.name)

    def test_file_is_loaded_from_web(self):
        url = 'http://www.example.com'
        self._osm_importer.load(url)

        openstreetmap.urlopen.assert_called_once_with(url)

    def test_tag_filter_removes_uninteresting_tags(self):
        tags = {'foo': 'bar'}
        self._osm_importer.filter_tags(tags)
        self.assertNotIn(('foo', 'bar'), tags.items())

    def test_tag_filter_does_not_touch_interesting_tags(self):
        tags = {'atm': 'yes'}
        self._osm_importer.filter_tags(tags)
        self.assertIn(('atm', 'yes'), tags.items())

    def test_tag_filter_keeps_all_tags_when_one_is_interesting(self):
        tags = {'atm': 'yes', 'opening_hours': 'foo'}
        self._osm_importer.filter_tags(tags)
        self.assertIn(('opening_hours', 'foo'), tags.items())

    def test_yielding_way_adds_it_with_points(self):
        poi = self._get_way_poi()
        self.assertTrue(Polygon(((2, 3), (3, 3), (3, 2))).equals(poi.geography))

    def test_open_ways_are_added_as_linestrings(self):
        poi = self._get_way_poi([1, 2, 3])
        self.assertTrue(LineString(((2, 3), (3, 3), (3, 2))).equals(poi.geography))

    def test_ways_with_no_tags_are_not_added(self):
        self._osm_importer.handle_ways([(12345, {}, [])])
        self.assertEquals(0, len(self._osm_importer.pois))

    def test_nodes_are_added(self):
        poi = self._get_node_poi()
        self.assertTrue(Point(2, 3).equals(poi.geography))

    def test_node_has_correct_uri(self):
        poi = self._get_node_poi()
        self.assertEquals('/osm:N12345', poi.uri)

    def test_way_has_correct_uri(self):
        poi = self._get_way_poi()
        self.assertEquals('/osm:W12345', poi.uri)

    def _get_node_poi(self):
        self._osm_importer.handle_nodes([(12345, {'atm': 'yes'}, (2, 3))])
        return self._osm_importer.pois[0]

    def _get_way_poi(self, coord_ids=(1, 2, 3, 1)):
        self._osm_importer.handle_coords([(1, 2, 3), (2, 3, 3), (3, 3, 2)])
        self._osm_importer.handle_ways([(12345, {'atm': 'yes'}, coord_ids)])
        return self._osm_importer.pois[0]
