import json
from mock import Mock
import unittest2 as unittest

from molly.apps.homepage.endpoints import HomepageEndpoint

class EndpointTestCase(unittest.TestCase):

    APP_MODULE = 'molly.test'
    APP_INSTANCE_NAME = 'test'
    APP_WIDGET_PARAMS = {'foo': 'bar'}
    APP_INDEX_URL = '/foo'
    HUMAN_NAME = 'Test'

    def test_response_includes_apps_list(self):
        self.assertEquals(1, len(self._get_response_dict()))

    def test_response_includes_app_data(self):
        app = self._get_response_dict()[0]
        self.assertEquals(self.APP_MODULE, app['module'])
        self.assertEquals(self.APP_INSTANCE_NAME, app['instance_name'])
        self.assertEquals(self.APP_WIDGET_PARAMS, app['widget_params'])
        self.assertEquals(self.HUMAN_NAME, app['human_name'])
        self.assertEquals(self.APP_INDEX_URL, app['index_url'])

    def test_response_has_correct_mime_type(self):
        response = HomepageEndpoint([]).get()
        self.assertEquals("application/json", response.headers.get('Content-Type'))

    def _get_response_dict(self):
        apps = [self._build_mock_app()]
        self._endpoint = HomepageEndpoint(apps)
        return json.loads(self._endpoint.get().data).get('applications')

    def _build_mock_app(self):
        app = Mock()
        app.module = self.APP_MODULE
        app.instance_name = self.APP_INSTANCE_NAME
        app.human_name = self.HUMAN_NAME
        app.homepage_widget_params = self.APP_WIDGET_PARAMS
        app.index_url = self.APP_INDEX_URL
        return app
