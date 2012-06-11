import unittest2 as unittest
from tch.source import Source

class SourceTest(unittest.TestCase):

    _TEST_URL = "http://www.naptan.org.uk/"
    _TEST_VERSION = 6

    def test_url_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('url', source_dict)
        self.assertEquals(self._TEST_URL, source_dict['url'])

    def test_version_in_serialised_source(self):
        source_dict = self._get_test_source_dict()

        self.assertIn('version', source_dict)
        self.assertEquals(self._TEST_VERSION, source_dict['version'])

    def _get_test_source_dict(self):
        source = Source()
        source.url = self._TEST_URL
        source.version = self._TEST_VERSION
        return source.as_dict()