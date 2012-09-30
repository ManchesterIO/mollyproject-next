# coding=utf-8
import unittest2 as unittest

from flask import Flask
from flaskext.babel import Babel

from molly.apps.weather import App as WeatherApp

class WeatherAppTest(unittest.TestCase):

    def setUp(self):
        self._app = Flask(__name__)
        self._babel = Babel(self._app)
        self._weather_app = WeatherApp('weather', {})
        self._app.register_blueprint(self._weather_app.blueprint, url_prefix="/weather")

    def test_module_is_set_correctly(self):
        self.assertEquals('molly.apps.weather', self._weather_app.module)

    def test_instance_name_is_set_correctly(self):
        self.assertEquals('weather', self._weather_app.instance_name)

    def test_human_name_is_set_correctly(self):
        self.assertEquals('Weather', self._weather_app.human_name)

    def test_human_name_is_i18n(self):
        with self._app.test_request_context('/'):
            self._babel.localeselector(lambda: 'fr')
            self.assertEquals(u'Météo', unicode(self._weather_app.human_name))

    def test_index_url_is_correct(self):
        with self._app.test_request_context('/'):
            self.assertEquals('/weather/', self._weather_app.index_url)
