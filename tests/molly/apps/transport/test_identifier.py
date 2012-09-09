import unittest2 as unittest
from tch.identifier import Identifier

class IdentifierTest(unittest.TestCase):

    _TEST_NS = "http://www.naptan.org.uk/"
    _TEST_VALUE = "9400ZZMAMCU"
    _TEST_LANG = "en"

    def test_ns_in_serialised_identifier(self):
        identifier_dict = self._get_test_identifier_dict()

        self.assertIn('namespace', identifier_dict)
        self.assertEquals(self._TEST_NS, identifier_dict['namespace'])

    def test_value_in_serialised_identifier(self):
        identifier_dict = self._get_test_identifier_dict()

        self.assertIn('value', identifier_dict)
        self.assertEquals(self._TEST_VALUE, identifier_dict['value'])

    def test_lang_in_serialised_identifier(self):
        identifier_dict = self._get_test_identifier_dict()

        self.assertIn('lang', identifier_dict)
        self.assertEquals(self._TEST_LANG, identifier_dict['lang'])

    def test_lang_omitted_when_lang_unset(self):
        identifier = self._get_test_identifier(lang=None)

        identifier_dict = identifier.as_dict()

        self.assertNotIn('lang', identifier_dict)

    def test_two_identifier_identifiers_are_equal(self):
        self.assertEqual(self._get_test_identifier(), self._get_test_identifier())
        self.assertFalse(self._get_test_identifier() != self._get_test_identifier())

    def test_two_different_identifiers_are_not_equal(self):
        identifier1 = self._get_test_identifier()
        identifier2 = self._get_test_identifier(value="foo bar")

        self.assertNotEqual(identifier1, identifier2)
        self.assertFalse(identifier1 == identifier2)

    def test_identifiers_are_immutable(self):
        identifier = self._get_test_identifier()
        try:
            identifier.value = "something different"
        except AttributeError:
            pass
        else:
            self.fail("Attribute error not raised")

    def _get_test_identifier(self, namespace=_TEST_NS, value=_TEST_VALUE,
                             lang=_TEST_LANG):
        return Identifier(namespace, value, lang)

    def _get_test_identifier_dict(self):
        return self._get_test_identifier().as_dict()
