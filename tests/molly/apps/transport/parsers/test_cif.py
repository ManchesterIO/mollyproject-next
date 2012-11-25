import mock
import os
import unittest2 as unittest

from tch.identifier import Identifier
from tch.parsers.cif import CifParser
from tch.stop import CallingPoint, TIPLOC_NAMESPACE, STANOX_NAMESPACE, CRS_NAMESPACE, CIF_DESCRIPTION_NAMESPACE

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

    def test_parser_yields_tiplocs(self):
        self.assertEquals(9, len(self._parser.tiplocs))

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
        self.assertEqual("Creative Commons Attribution-ShareAlike", self._parser.tiplocs[0].sources.pop().licence)

    def test_licence_url_is_correctly_set_on_tiploc(self):
        self.assertEqual(
            "http://creativecommons.org/licenses/by-sa/1.0/legalcode",
            self._parser.tiplocs[0].sources.pop().licence_url
        )

    def test_attribution_is_correctly_set_on_tiploc(self):
        self.assertEqual(
            '<a href="http://www.atoc.org/">Source: RSP</a>',
            self._parser.tiplocs[0].sources.pop().attribution
        )

