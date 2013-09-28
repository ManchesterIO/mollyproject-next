import unittest2 as unittest

from molly.ui.html5.filters import ui_url


class UiUrlFilterTest(unittest.TestCase):

    def test_correct_url_is_returned(self):
        self.assertEquals('/foo/bar', ui_url('http://localhost:8000/foo/bar'))