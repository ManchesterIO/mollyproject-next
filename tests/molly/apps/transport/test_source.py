import unittest2 as unittest
from tch.source import Source

class SourceTest(unittest.TestCase):

    _TEST_URL = "http://www.naptan.org.uk/"
    _TEST_VERSION = 6
    _TEST_ATTRIBUTION = "attribution"
    _TEST_LICENCE = "Open Government Licence"
    _TEST_LICENCE_URI = "http://www.example.com/"

    def test_url_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('url', source_dict)
        self.assertEquals(self._TEST_URL, source_dict['url'])

    def test_version_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('version', source_dict)
        self.assertEquals(self._TEST_VERSION, source_dict['version'])

    def test_attribution_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('attribution', source_dict)
        self.assertEquals(self._TEST_ATTRIBUTION, source_dict['attribution'])

    def test_licence_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('licence', source_dict)
        self.assertEquals(self._TEST_LICENCE, source_dict['licence'])

    def test_licence_url_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('licence_url', source_dict)
        self.assertEquals(self._TEST_LICENCE_URI, source_dict['licence_url'])

    def test_two_sources_are_equal(self):
        self.assertEqual(self._get_test_source(), self._get_test_source())

    def _get_test_source_dict(self):
        return self._get_test_source().as_dict()

    def _get_test_source(self):
        source = Source()
        source.url = self._TEST_URL
        source.version = self._TEST_VERSION
        source.attribution = self._TEST_ATTRIBUTION
        source.licence = self._TEST_LICENCE
        source.licence_url = self._TEST_LICENCE_URI
        return source
