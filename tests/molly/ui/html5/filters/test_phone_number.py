import unittest2 as unittest

from molly.ui.html5.filters.phone_number import format_telephone_number


class PhoneNumberFilterTest(unittest.TestCase):

    def test_phone_number_formats_correctly(self):
        self.assertEquals(
            '020 8811 8181',
            format_telephone_number('+442088118181')
        )

    def test_unparseable_phone_numbers_pass_straight_through(self):
        self.assertEquals('hello world', format_telephone_number('hello world'))