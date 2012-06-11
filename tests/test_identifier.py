import unittest2 as unittest
from tch.identifier import Identifier
from tch.source import Source

class SourceTest(unittest.TestCase):

    _TEST_NS = "http://www.naptan.org.uk/"
    _TEST_VALUE = "9400ZZMAMCU"

    def test_ns_in_serialised_identifier(self):
        identifier_dict = self._get_test_identifier_dict()

        self.assertIn('namespace', identifier_dict)
        self.assertEquals(self._TEST_NS, identifier_dict['namespace'])

    def test_value_in_serialised_identifier(self):
        identifier_dict = self._get_test_identifier_dict()

        self.assertIn('value', identifier_dict)
        self.assertEquals(self._TEST_VALUE, identifier_dict['value'])

    def _get_test_identifier_dict(self):
        identifier = Identifier()
        identifier.namespace = self._TEST_NS
        identifier.value = self._TEST_VALUE
        return identifier.as_dict()