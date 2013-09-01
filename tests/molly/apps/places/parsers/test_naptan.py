import os
import unittest2 as unittest
from molly.apps.common.components import Identifier
from molly.apps.places.models import PointOfInterest, ATCO_NAMESPACE, CRS_NAMESPACE, TIPLOC_NAMESPACE
from molly.apps.places.parsers.naptan import NaptanParser


class NaptanParserTest(unittest.TestCase):

    _TEST_URL = 'http://www.naptan.com'

    def setUp(self):
        self._test_file = open(os.path.join(os.path.dirname(__file__), 'naptan_testdata', 'naptan.xml'))

    def tearDown(self):
        self._test_file.close()

    def test_bus_stop_yields_point_of_interest(self):
        stops = self._import_from_test_data()
        self.assertIsInstance(stops.next(), PointOfInterest)

    def test_bus_stop_source_url_is_set_correctly(self):
        self.assertEquals(self._TEST_URL + "/NaPTAN.xml", self._get_bus_stop().sources.pop().url)

    def test_bus_stop_source_version_is_set_correctly(self):
        self.assertEquals('2', self._get_bus_stop().sources.pop().version)

    def test_licence_is_correctly_set_on_bus_stop(self):
        self.assertEqual("Open Government Licence", self._get_bus_stop().sources.pop().attribution.licence_name)

    def test_licence_url_is_correctly_set_on_bus_stop(self):
        self.assertEqual("http://www.nationalarchives.gov.uk/doc/open-government-licence/",
            self._get_bus_stop().sources.pop().attribution.licence_url)

    def test_attribution_is_correctly_set_on_bus_stop(self):
        self.assertEqual("Contains public sector information licensed under the Open Government Licence v1.0",
            self._get_bus_stop().sources.pop().attribution.attribution_text)

    def test_bus_stop_has_correct_slug(self):
        self.assertEquals('atco:639000011', self._get_bus_stop().slug)

    def test_second_bus_stop_has_correct_slug(self):
        bus_stop = list(self._import_from_test_data())[1]
        self.assertEquals('atco:639000012', bus_stop.slug)

    def test_taxi_ranks_are_yielded(self):
        self.assertIn('atco:6490TX001', self._get_stops_by_slugs().keys())

    def test_single_terminal_airports_are_yielded_as_points_of_interest(self):
        stops_dict = self._get_stops_by_slugs()
        self.assertIsInstance(stops_dict['atco:9200ABZ1'], PointOfInterest)

    def test_ferry_terminals_are_yielded_as_stops(self):
        stops_dict = self._get_stops_by_slugs()
        self.assertIsInstance(stops_dict['atco:9300ACH'], PointOfInterest)

    def test_things_without_revision_numbers_default_to_0(self):
        stops_dict = self._get_stops_by_slugs()
        stop = stops_dict['atco:6490IM1778']
        self.assertEquals('0', stop.sources.pop().version)

    def test_rail_stations_get_stop_and_calling_point(self):
        stops = self._get_stops_by_slugs()
        self.assertIn('atco:9100ABDARE', stops)

    def test_metro_stations_are_yielded(self):
        stops = self._get_stops_by_slugs()
        self.assertIsInstance(stops['atco:9400ZZALGWP'], PointOfInterest)

    def test_bus_stations_bays_are_yielded_as_points_of_interest(self):
        stops = self._get_stops_by_slugs()
        self.assertIsInstance(stops['atco:639070011'], PointOfInterest)

    def test_bus_stations_variable_bays_are_yielded_as_calling_points(self):
        stops = self._get_stops_by_slugs()
        self.assertIsInstance(stops['atco:1400LE0400'], PointOfInterest)

    def test_atco_code_is_an_identifier(self):
        stops = self._get_stops_by_slugs()
        self.assertIn(Identifier(namespace=ATCO_NAMESPACE, value='9100ABDARE') , stops['atco:9100ABDARE'].identifiers)

    def test_crs_code_is_an_identifier(self):
        stops = self._get_stops_by_slugs()
        self.assertIn(Identifier(namespace=CRS_NAMESPACE, value='ABA') , stops['atco:9100ABDARE'].identifiers)

    def test_tiploc_code_is_an_identifier(self):
        stops = self._get_stops_by_slugs()
        self.assertIn(Identifier(namespace=TIPLOC_NAMESPACE, value='ABDARE') , stops['atco:9100ABDARE'].identifiers)

    def _import_from_test_data(self):
        return NaptanParser().import_from_file(self._test_file, self._TEST_URL)

    def _get_bus_stop(self):
        return self._import_from_test_data().next()

    def _get_stops_by_slugs(self):
        stops = list(self._import_from_test_data())
        return dict(zip(map(lambda s: s.slug, stops), stops))
