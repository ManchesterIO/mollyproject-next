import os
import unittest2 as unittest
from tch.parsers.naptan import NaptanParser
from tch.stop import CallingPoint, Stop, Interchange

class NaptanParserTest(unittest.TestCase):

    _TEST_URL = 'http://www.naptan.com'

    def setUp(self):
        self._test_file = open(os.path.join(os.path.dirname(__file__), 'naptan_testdata', 'naptan.xml'))

    def tearDown(self):
        self._test_file.close()

    def test_bus_stop_yields_stop_and_calling_point(self):
        stops = self._import_from_test_data()
        self.assertIsInstance(stops.next(), Stop)
        self.assertIsInstance(stops.next(), CallingPoint)

    def test_bus_stop_source_url_is_set_correctly(self):
        self.assertEquals(self._TEST_URL + "/NaPTAN.xml", self._get_bus_stop().sources[0].url)

    def test_bus_stop_source_version_is_set_correctly(self):
        self.assertEquals('2', self._get_bus_stop().sources[0].version)

    def test_licence_is_correctly_set_on_bus_stop(self):
        self.assertEqual("Open Government Licence", self._get_bus_stop().sources[0].licence)

    def test_licence_url_is_correctly_set_on_bus_stop(self):
        self.assertEqual("http://www.nationalarchives.gov.uk/doc/open-government-licence/",
            self._get_bus_stop().sources[0].licence_url)

    def test_attribution_is_correctly_set_on_bus_stop(self):
        self.assertEqual("Contains public sector information licensed under the Open Government Licence v1.0",
            self._get_bus_stop().sources[0].attribution)

    def test_bus_calling_point_source_url_is_set_correctly(self):
        self.assertEquals(self._TEST_URL + "/NaPTAN.xml", self._get_bus_calling_point().sources[0].url)

    def test_bus_stop_has_correct_url(self):
        self.assertEquals('/gb/639000011', self._get_bus_stop().url)

    def test_bus_calling_point_has_correct_url(self):
        self.assertEquals('/gb/639000011/calling_point', self._get_bus_calling_point().url)

    def test_second_bus_stop_has_correct_url(self):
        bus_stop = list(self._import_from_test_data())[2]
        self.assertEquals('/gb/639000012', bus_stop.url)

    def test_bus_calling_point_has_stop_as_parent(self):
        self.assertEquals('/gb/639000011', self._get_bus_calling_point().parent_stop)

    def test_bus_stop_has_calling_point_as_child(self):
        self.assertEquals(['/gb/639000011/calling_point'], self._get_bus_stop().calling_points)

    def test_taxi_ranks_are_not_yielded(self):
        self.assertNotIn('/gb/6490TX001', self._get_stops_by_url().keys())

    def test_single_terminal_airports_are_yielded_as_stops(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9200ABZ1'], Stop)

    def test_multiple_terminal_airports_are_returned_as_interchange(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9200MAN0'], Interchange)

    def _import_from_test_data(self):
        return NaptanParser().import_from_file(self._test_file, self._TEST_URL)

    def _get_bus_stop(self):
        return self._import_from_test_data().next()

    def _get_bus_calling_point(self):
        return list(self._import_from_test_data())[1]

    def _get_stops_by_url(self):
        stops = list(self._import_from_test_data())
        return dict(zip(map(lambda s: s.url, stops), stops))

if __name__ == '__main__':
    unittest.main()
