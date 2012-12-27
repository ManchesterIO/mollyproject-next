# coding=utf-8
from mock import Mock, sentinel
import unittest2 as unittest

from flask import Flask
from flaskext.babel import Babel

from molly.apps import weather

class WeatherAppTest(unittest.TestCase):

    _OBSERVATION = {'hello': 'world'}

    def setUp(self):
        self._provider = Mock()
        self._provider.latest_observations = Mock(return_value=self._OBSERVATION)
        self._observations_endpoint = Mock()
        self._observations_endpoint.get.methods = ('GET',)
        self._observations_endpoint.get.required_methods = ()
        weather.ObservationsEndpoint = Mock(return_value=self._observations_endpoint)
        self._weather_app = weather.App('weather', {}, [self._provider], {})

    def test_module_is_set_correctly(self):
        self.assertEquals('http://mollyproject.org/apps/weather', self._weather_app.module)

    def test_instance_name_is_set_correctly(self):
        self.assertEquals('weather', self._weather_app.instance_name)

    def test_human_name_is_set_correctly(self):
        self.assertEquals('Weather', self._weather_app.human_name)

    def test_human_name_is_i18n(self):
        app = self._get_flask()
        babel = Babel(app)
        with app.test_request_context('/'):
            babel.localeselector(lambda: 'fr')
            self.assertEquals(u'Météo', unicode(self._weather_app.human_name))

    def test_latest_observations_are_used_in_link(self):
        expected = sentinel.expected_endpoint
        self._observations_endpoint.component.return_value = expected
        self.assertEquals([expected], self._weather_app.links)

    def _get_flask(self):
        app = Flask(__name__)
        app.register_blueprint(self._weather_app.blueprint, url_prefix="/weather")
        return app
