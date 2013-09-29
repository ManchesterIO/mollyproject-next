from flask import Flask
from flask.ext.babel import Babel
import unittest2 as unittest

from molly.ui.html5.filters import humanise_distance


class HumaniseDistanceFilterTest(unittest.TestCase):

    def test_small_distances_returned_in_metres(self):
        flask_app = Flask(__name__)
        Babel(flask_app)
        with flask_app.test_request_context():
            self.assertEquals("6m", humanise_distance(6))

    def test_long_distances_returned_in_miles(self):
        flask_app = Flask(__name__)
        Babel(flask_app)
        with flask_app.test_request_context():
            self.assertEquals("2.6 miles", humanise_distance(4184))
