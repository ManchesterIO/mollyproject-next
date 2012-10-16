import json
from flask import Flask
from mock import Mock
import unittest2 as unittest
from werkzeug.exceptions import NotAcceptable

from molly.apps.homepage.endpoints import HomepageEndpoint

class EndpointTestCase(unittest.TestCase):

    APP_MODULE = 'http://example.com/test'
    APP_INSTANCE_NAME = 'test'
    APP_LINKS = [{}]
    HUMAN_NAME = 'Test'

    def test_response_includes_apps_list(self):
        self.assertEquals(1, len(self._get_apps_dict()))

    def test_response_includes_app_data(self):
        app = self._get_apps_dict()[0]
        self.assertEquals(self.APP_MODULE, app['self'])
        self.assertEquals(self.APP_INSTANCE_NAME, app['instance_name'])
        self.assertEquals(self.APP_LINKS, app['links'])
        self.assertEquals(self.HUMAN_NAME, app['human_name'])

    def test_response_has_correct_mime_type(self):
        with Flask(__name__).test_request_context('/', headers=[('Accept', 'application/json')]):
            response = HomepageEndpoint([]).get()
        self.assertEquals("application/json", response.headers.get('Content-Type'))

    def test_json_responses_throw_406_error(self):
        with Flask(__name__).test_request_context('/'):
            self.assertRaises(NotAcceptable, HomepageEndpoint([]).get)

    def test_response_includes_self(self):
        response = self._get_response_dict()
        self.assertEquals('http://mollyproject.org/apps/homepage', response['self'])

    def _get_response_dict(self):
        apps = [self._build_mock_app()]
        flask_app = Flask(__name__)
        with flask_app.test_request_context('/', headers=[('Accept', 'application/json')]):
            self._endpoint = HomepageEndpoint(apps)
            return json.loads(self._endpoint.get().data)

    def _get_apps_dict(self):
        return self._get_response_dict().get('applications')

    def _build_mock_app(self):
        app = Mock()
        app.module = self.APP_MODULE
        app.instance_name = self.APP_INSTANCE_NAME
        app.human_name = self.HUMAN_NAME
        app.links = self.APP_LINKS
        return app
