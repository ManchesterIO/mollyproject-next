import os
import unittest2 as unittest
from tch.parsers.naptan import NaptanParser
from tch.stop import CallingPoint, Stop

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
        self.assertEquals({'/gb/639000011/calling_point'}, self._get_bus_stop().calling_points)

    def test_taxi_ranks_are_not_yielded(self):
        self.assertNotIn('/gb/6490TX001', self._get_stops_by_url().keys())

    def test_single_terminal_airports_are_yielded_as_stops(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9200ABZ1'], Stop)

    def test_single_terminal_airports_have_a_calling_point(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9200ABZ1/calling_point'], CallingPoint)

    def test_airport_terminals_are_yielded_as_calling_points(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9200MAN1'], CallingPoint)

    def test_airport_terminals_have_airport_as_parent(self):
        terminal = self._get_stops_by_url()['/gb/9200MAN1']
        self.assertEquals('/gb/9200MAN0', terminal.parent_stop)

    def test_airports_have_terminals_as_calling_points(self):
        airport = self._get_stops_by_url()['/gb/9200MAN0']
        self.assertEquals(
            {'/gb/9200MAN1', '/gb/9200MAN2', '/gb/9200MAN3'},
            airport.calling_points
        )

    def test_airports_with_terminals_do_not_have_own_calling_point(self):
        self.assertNotIn('/gb/9200MAN0/calling_point', self._get_stops_by_url())

    def test_airport_calling_point_has_correct_parent(self):
        stops = self._get_stops_by_url()
        self.assertEquals('/gb/9200ABZ1', stops['/gb/9200ABZ1/calling_point'].parent_url)

    def test_airport_with_no_terminals_includes_calling_points(self):
        stops = self._get_stops_by_url()
        self.assertEquals({'/gb/9200ABZ1/calling_point'}, stops['/gb/9200ABZ1'].calling_points)

    def test_ferry_terminals_are_yielded_as_stops(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9300ACH'], Stop)

    def test_ferry_berths_are_yielded_as_calling_points(self):
        stops_dict = self._get_stops_by_url()
        self.assertIsInstance(stops_dict['/gb/9300MTS1'], CallingPoint)

    def test_berthless_ferry_terminals_have_generated_calling_point(self):
        stops_dict = self._get_stops_by_url()
        stop = stops_dict['/gb/9300ACH']
        calling_point_url = stop.calling_points.pop()
        self.assertIsInstance(stops_dict[calling_point_url], CallingPoint)

    def test_ferry_terminals_with_berths_have_calling_point_from_naptan(self):
        stops_dict = self._get_stops_by_url()
        stop = stops_dict['/gb/9300MTS']
        self.assertEquals(1, len(stop.calling_points))
        self.assertEquals({'/gb/9300MTS1'}, stop.calling_points)

    def test_things_without_revision_numbers_default_to_0(self):
        stops_dict = self._get_stops_by_url()
        stop = stops_dict['/gb/6490IM1778']
        self.assertEquals('0', stop.sources[0].version)

    def test_ferry_terminals_without_stop_area_imply_group(self):
        stops_dict = self._get_stops_by_url()
        stop = stops_dict['/gb/9300EIB']
        self.assertEquals(1, len(stop.calling_points))
        self.assertEquals({'/gb/9300EIB1'}, stop.calling_points)

    def test_berths_have_terminal_as_parent_stop(self):
        stops_dict = self._get_stops_by_url()
        stop = stops_dict['/gb/9300MTS1']
        self.assertEquals('/gb/9300MTS', stop.parent_stop)

    def test_rail_stations_get_stop_and_calling_point(self):
        stops = self._get_stops_by_url()
        self.assertIn('/gb/9100ABDARE', stops)
        self.assertIn('/gb/9100ABDARE/calling_point', stops)

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
