import mock
import os
import unittest2 as unittest
from molly.apps.common.components import Identifier
from molly.apps.transport.parsers.cif import CifParser
from molly.apps.transport.models import CallingPoint, TIPLOC_NAMESPACE, STANOX_NAMESPACE, CRS_NAMESPACE, CIF_DESCRIPTION_NAMESPACE, Call, CallTime

class CifParserTest(unittest.TestCase):

    def setUp(self):
        self._files_to_close = []
        self._mock_cif = mock.Mock()
        self._mock_cif.namelist = ['TEST.MCA']
        self._mock_cif.open = self._open_mock_file
        self._parser = CifParser()
        self._parser.import_from_file(self._mock_cif)

    def _open_mock_file(self, filename):
        fd = open(os.path.join(os.path.dirname(__file__), 'cif_testdata', filename))
        self._files_to_close.append(fd)
        return fd

    def tearDown(self):
        for fd in self._files_to_close:
            fd.close()

    def test_tiplocs_are_calling_points(self):
        for tiploc in self._parser.tiplocs:
            self.assertIsInstance(tiploc, CallingPoint)

    def test_tiploc_has_correct_tiploc(self):
        self.assertIn(Identifier(namespace=TIPLOC_NAMESPACE, value='AACHEN'), self._parser.tiplocs[0].identifiers)

    def test_tiploc_has_correct_stanox(self):
        self.assertIn(Identifier(namespace=STANOX_NAMESPACE, value='00005'), self._parser.tiplocs[0].identifiers)

    def test_tiploc_has_correct_crs(self):
        self.assertIn(Identifier(namespace=CRS_NAMESPACE, value='XPZ'), self._parser.tiplocs[2].identifiers)

    def test_tiploc_with_no_crs_does_not_contain_crs(self):
        self.assertNotIn(Identifier(namespace=CRS_NAMESPACE, value=""), self._parser.tiplocs[0].identifiers)

    def test_tiploc_has_titlecased_description(self):
        self.assertIn(
            Identifier(namespace=CIF_DESCRIPTION_NAMESPACE, value="Aachen"),
            self._parser.tiplocs[0].identifiers
        )

    def test_tiploc_source_url_is_set_correctly(self):
            self.assertEquals("cif:", self._parser.tiplocs[0].sources.pop().url)

    def test_tiploc_source_version_is_set_correctly(self):
        self.assertEquals('TEST', self._parser.tiplocs[0].sources.pop().version)

    def test_licence_is_correctly_set_on_tiploc(self):
        self.assertEquals(
            "Creative Commons Attribution-ShareAlike",
            self._parser.tiplocs[0].sources.pop().attribution.licence_name
        )

    def test_licence_url_is_correctly_set_on_tiploc(self):
        self.assertEquals(
            "http://creativecommons.org/licenses/by-sa/1.0/legalcode",
            self._parser.tiplocs[0].sources.pop().attribution.licence_url
        )

    def test_attribution_is_correctly_set_on_tiploc(self):
        source = self._parser.tiplocs[0].sources.pop()
        self.assertEquals('Source: RSP', source.attribution.attribution_text)
        self.assertEquals('http://www.atoc.org/', source.attribution.attribution_url)

    def test_route_name_is_correctly_defined(self):
        self.assertEquals('Crewe to Derby', self._parser.services[0].name)

    def test_route_slug_is_set(self):
        self.assertEquals('/gb/rail/CREWE-DRBY', self._parser.routes[0].slug)

    def test_return_journey_is_correctly_grouped_into_one_service(self):
        self.assertEquals(self._parser.services[0].routes, {'/gb/rail/CREWE-DRBY', '/gb/rail/DRBY-CREWE'})
        self.assertEquals(self._parser.routes[0].service_slug, self._parser.routes[1].service_slug)

    def test_service_has_correct_slug(self):
        self.assertEquals('/gb/rail/CREWE-DRBY', self._parser.services[0].slug)

    def test_routes_have_service_slug(self):
        self.assertEquals('/gb/rail/CREWE-DRBY', self._parser.routes[0].service_slug)

    def test_route_variations_are_correctly_identified(self):
        self.assertEquals(4, len(self._parser.routes))

    def test_scheduled_trips_use_uid_as_slug(self):
        self.assertEquals('/gb/rail/C03360', self._parser.scheduled_trips[0].slug)

    def test_routes_contain_correctly_ordered_slugs(self):
        self.assertEquals([
            '/gb/9400CREWE/calling_point',
            '/gb/9400CREWSJN/calling_point',
            '/gb/9400BTHLYJN/calling_point',
            '/gb/9400ALSAGER/calling_point',
            '/gb/9400KIDSGRV/calling_point',
            '/gb/9400LNGP/calling_point',
            '/gb/9400STOKEOT/calling_point',
            '/gb/9400STOKOTJ/calling_point',
            '/gb/9400LNTN/calling_point',
            '/gb/9400CAVRSWL/calling_point',
            '/gb/9400BLYBDGE/calling_point',
            '/gb/9400UTOXSB/calling_point',
            '/gb/9400UTOXETR/calling_point',
            '/gb/9400TUTBURY/calling_point',
            '/gb/9400NSJDRBY/calling_point',
            '/gb/9400STSNJN/calling_point',
            '/gb/9400DRBY/calling_point'
        ], self._parser.routes[0].calling_points)

    def test_route_headline_is_destination(self):
        self.assertEquals('Derby', self._parser.routes[0].headline)

    def test_trips_have_correct_route(self):
        self.assertEquals('/gb/rail/CREWE-DRBY', self._parser.scheduled_trips[0].route_slug)

    def test_platforms_get_own_calling_points(self):
        self.assertEquals('/gb/9400CREWE/platform4', self._parser.tiplocs[68].slug)

    def test_platforms_have_parent_station(self):
        self.assertEquals('/gb/9400CREWE', self._parser.tiplocs[68].parent_slug)

    def test_scheduled_journeys_correctly_populated(self):
        self.assertEquals(
            [
                Call(
                    point_slug='/gb/9400CREWE/platform4',
                    scheduled_departure_time=CallTime(15, 5),
                    public_departure_time=CallTime(15, 5),
                    activity=Call.START
                ),
                Call(
                    point_slug='/gb/9400CREWSJN/platformUDP',
                    scheduled_arrival_time=CallTime(15, 8),
                    scheduled_departure_time=CallTime(15, 8),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400BTHLYJN/calling_point',
                    scheduled_arrival_time=CallTime(15, 11),
                    scheduled_departure_time=CallTime(15, 11),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400ALSAGER/calling_point',
                    scheduled_arrival_time=CallTime(15, 14),
                    public_arrival_time=CallTime(15, 14),
                    scheduled_departure_time=CallTime(15, 14, 30),
                    public_departure_time=CallTime(15, 14),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400KIDSGRV/calling_point',
                    scheduled_arrival_time=CallTime(15, 21),
                    public_arrival_time=CallTime(15, 21),
                    scheduled_departure_time=CallTime(15, 21, 30),
                    public_departure_time=CallTime(15, 21),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400LNGP/calling_point',
                    scheduled_arrival_time=CallTime(15, 26),
                    public_arrival_time=CallTime(15, 26),
                    scheduled_departure_time=CallTime(15, 26, 30),
                    public_departure_time=CallTime(15, 26),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400STOKEOT/platform1',
                    scheduled_arrival_time=CallTime(15, 31),
                    public_arrival_time=CallTime(15, 30),
                    scheduled_departure_time=CallTime(15, 32),
                    public_departure_time=CallTime(15, 32),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400STOKOTJ/calling_point',
                    scheduled_arrival_time=CallTime(15, 33, 30),
                    scheduled_departure_time=CallTime(15, 33, 30),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400LNTN/calling_point',
                    scheduled_arrival_time=CallTime(15, 37, 30),
                    public_arrival_time=CallTime(15, 38),
                    scheduled_departure_time=CallTime(15, 38),
                    public_departure_time=CallTime(15, 38),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400CAVRSWL/calling_point',
                    scheduled_arrival_time=CallTime(15, 42),
                    scheduled_departure_time=CallTime(15, 42),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400BLYBDGE/calling_point',
                    scheduled_arrival_time=CallTime(15, 43, 30),
                    public_arrival_time=CallTime(15, 43),
                    scheduled_departure_time=CallTime(15, 44, 30),
                    public_departure_time=CallTime(15, 44),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400UTOXSB/calling_point',
                    scheduled_arrival_time=CallTime(15, 54, 30),
                    scheduled_departure_time=CallTime(15, 54, 30),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400UTOXETR/calling_point',
                    scheduled_arrival_time=CallTime(15, 56),
                    public_arrival_time=CallTime(15, 56),
                    scheduled_departure_time=CallTime(15, 56, 30),
                    public_departure_time=CallTime(15, 56),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400TUTBURY/calling_point',
                    scheduled_arrival_time=CallTime(16, 05),
                    public_arrival_time=CallTime(16, 05),
                    scheduled_departure_time=CallTime(16, 06),
                    public_departure_time=CallTime(16, 06),
                    activity=Call.NORMAL
                ),
                Call(
                    point_slug='/gb/9400NSJDRBY/calling_point',
                    scheduled_arrival_time=CallTime(16, 13, 30),
                    scheduled_departure_time=CallTime(16, 13, 30),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400STSNJN/calling_point',
                    scheduled_arrival_time=CallTime(16, 14, 30),
                    scheduled_departure_time=CallTime(16, 14, 30),
                    activity=Call.PASS_THROUGH
                ),
                Call(
                    point_slug='/gb/9400DRBY/platform1',
                    scheduled_arrival_time=CallTime(16, 22),
                    public_arrival_time=CallTime(16, 25),
                    activity=Call.FINISH
                ),
            ],
            self._parser.scheduled_trips[0].calling_points
        )

    # TODO: Detecting and populating of vias
    # TODO: Operating period setting
    # TODO: Journeys across midnight
    # TODO: Associations
    # TODO: TIPLOC URL and mapping to parents
