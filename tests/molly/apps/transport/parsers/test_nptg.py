import os
from shapely.geometry.point import Point
import unittest2 as unittest
from molly.apps.common.components import Identifier, LocalisedName
from molly.apps.transport.models import NPTG_REGION_CODE_NAMESPACE, NPTG_DISTRICT_CODE_NAMESPACE, NPTG_LOCALITY_CODE_NAMESPACE
from molly.apps.transport.parsers.nptg import NptgParser

class NptgParserTest(unittest.TestCase):

    _TEST_URL = "http://nptg/test"

    def setUp(self):
        self._test_file = open(os.path.join(os.path.dirname(__file__), 'nptg_testdata', 'nptg.xml'))

    def tearDown(self):
        self._test_file.close()

    def test_source_is_correctly_set_on_localities(self):
        locality = self._import_from_test_data().next()
        self.assertEqual(self._TEST_URL + "/NPTG.xml", locality.sources[0].url)

    def test_licence_is_correctly_set_on_localities(self):
        locality = self._import_from_test_data().next()
        self.assertEqual("Open Government Licence", locality.sources[0].attribution.licence_name)

    def test_licence_url_is_correctly_set_on_localities(self):
        locality = self._import_from_test_data().next()
        self.assertEqual("http://www.nationalarchives.gov.uk/doc/open-government-licence/",
            locality.sources[0].attribution.licence_url)

    def test_attribution_is_correctly_set_on_localities(self):
        locality = self._import_from_test_data().next()
        self.assertEqual("Contains public sector information licensed under the Open Government Licence v1.0",
            locality.sources[0].attribution.attribution_text)

    def test_parse_returns_correct_number_of_items(self):
        self.assertEqual(8, len(list(self._import_from_test_data())))

    def test_source_version_is_correctly_set_on_region(self):
        locality = self._get_imported_region()
        self.assertEqual("42", locality.sources[0].version)

    def test_region_url_is_derived_from_region_code(self):
        locality = self._get_imported_region()
        self.assertEqual("/gb/EA", locality.url)

    def test_region_code_is_identifier_on_region(self):
        expected_identifier = Identifier(namespace=NPTG_REGION_CODE_NAMESPACE, value="EA")
        locality = self._get_imported_region()
        self.assertIn(expected_identifier, locality.identifiers)

    def test_region_name_is_identifier_on_region(self):
        expected_identifier = LocalisedName(name="East Anglia", lang="en")
        locality = self._get_imported_region()
        self.assertIn(expected_identifier, locality.names)

    def test_multiple_region_names_are_set(self):
        expected_identifier = LocalisedName(name="Something in German", lang="de")
        locality = self._get_imported_region()
        self.assertIn(expected_identifier, locality.names)

    def test_version_is_set_on_district(self):
        self.assertEqual("2", self._get_imported_district().sources[0].version)

    def test_district_id_is_set_on_district(self):
        expected_identifier = Identifier(namespace=NPTG_DISTRICT_CODE_NAMESPACE, value='29')
        locality = self._get_imported_district()
        self.assertIn(expected_identifier, locality.identifiers)

    def test_name_is_set_on_district(self):
        expected_identifier = LocalisedName(name='Cambridge', lang='en')
        locality = self._get_imported_district()
        self.assertIn(expected_identifier, locality.names)

    def test_district_has_correct_parent(self):
        locality = self._get_imported_district()
        self.assertEqual("/gb/EA", locality.parent_url)

    def test_district_has_correct_url(self):
        locality = self._get_imported_district()
        self.assertEqual("/gb/29", locality.url)

    def test_imported_locality_has_correct_url(self):
        locality = self._get_imported_locality()
        self.assertEquals("/gb/E0034964", locality.url)

    def test_locality_code_is_set_on_locality(self):
        expected_identifier = Identifier(namespace=NPTG_LOCALITY_CODE_NAMESPACE, value='E0034964')
        locality = self._get_imported_locality()
        self.assertIn(expected_identifier, locality.identifiers)

    def test_locality_name_is_set_on_locality(self):
        expected_identifier = LocalisedName(name='Amesbury', lang='en')
        locality = self._get_imported_locality()
        self.assertIn(expected_identifier, locality.names)

    def test_locality_location_is_set(self):
        expected_location = Point(-2.4966503699, 51.3259016941)
        locality = self._get_imported_locality()
        self.assertEqual(expected_location.xy, locality.geography.xy)

    def test_locality_has_correct_parent(self):
        locality = self._get_imported_locality()
        self.assertEqual("/gb/310", locality.parent_url)

    def test_child_locality_has_correct_parent(self):
        locality = self._get_imported_child_locality()
        self.assertEqual("/gb/E0052932", locality.parent_url)

    def _import_from_test_data(self):
        nptg_parser = NptgParser()
        return nptg_parser.import_from_file(self._test_file, self._TEST_URL)

    def _get_imported_region(self):
        return list(self._import_from_test_data())[5]

    def _get_imported_district(self):
        return self._import_from_test_data().next()

    def _get_imported_locality(self):
        return list(self._import_from_test_data())[6]

    def _get_imported_child_locality(self):
        return list(self._import_from_test_data())[7]
