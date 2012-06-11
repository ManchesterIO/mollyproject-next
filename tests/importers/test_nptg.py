import os
import unittest2 as unittest

from tch.importers.nptg import NptgParser
from tch.locality import NPTG_REGION_CODE_NAMESPACE

class NptgParserTest(unittest.TestCase):

    _TEST_URL = "http://nptg/test"

    def setUp(self):
        self._test_file = open(os.path.join(os.path.dirname(__file__),
            'nptg_testdata', 'nptg.xml'))

    def tearDown(self):
        self._test_file.close()

    def test_source_is_correctly_set_on_localities(self):
        locality = self._import_from_test_data().next()
        self.assertEqual(self._TEST_URL + "/NPTG.xml", locality.sources[0].url)

    def test_parse_returns_correct_number_of_items(self):
        count = 0
        for locality in self._import_from_test_data():
            count += 1
        self.assertEqual(7, count)

    def test_source_version_is_correctly_set_on_region(self):
        locality = self._get_imported_region()
        self.assertEqual("42", locality.sources[0].version)

    def test_region_url_is_derived_from_region_code(self):
        locality = self._get_imported_region()
        self.assertEqual("/EA/", locality.url)

    def test_region_code_is_identifier_on_region(self):
        locality = self._get_imported_region()
        self.assertEqual("EA",
            locality.identifiers.by_namespace(NPTG_REGION_CODE_NAMESPACE))

    def _import_from_test_data(self):
        nptg_parser = NptgParser()
        return nptg_parser.import_from_file(self._test_file, self._TEST_URL)

    def _get_imported_region(self):
        return list(self._import_from_test_data())[5]