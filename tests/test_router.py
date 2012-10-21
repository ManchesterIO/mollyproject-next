from httplib import HTTPException
from mock import Mock, sentinel
import unittest2 as unittest
from werkzeug.exceptions import NotFound, ServiceUnavailable, BadGateway

from molly.ui.html5.router import Router

class RouterTest(unittest.TestCase):

    def setUp(self):
        self._request_factory = Mock()
        self._request_factory.request = Mock()
        self._request_factory.request.return_value = self.build_mock_response()
        self._component_factory = Mock()
        self._page_decorator = Mock()
        self._page_decorator_factory = Mock()
        self._page_decorator_factory.get_decorator = Mock(return_value=self._page_decorator)
        self._router = Router(self._request_factory, self._component_factory, self._page_decorator_factory)

    def test_calling_router_makes_appropriate_backend_request(self):
        self._router('')
        self._request_factory.request.assert_called_once_with('/')

    def test_404_response_from_backend_returns_404_to_frontend(self):
        self._request_factory.request.return_value = self.build_mock_response(status=404)

        self.assertIsInstance(self._router(''), NotFound)

    def test_not_connecting_to_backend_raises_503(self):
        self._request_factory.RequestException = HTTPException
        self._request_factory.request.side_effect = HTTPException()

        self.assertIsInstance(self._router(''), ServiceUnavailable)

    def test_non_json_response_returns_502(self):
        self._request_factory.request.return_value = self.build_mock_response(body='I am not JSON')
        self.assertIsInstance(self._router(''), BadGateway)

    def test_correct_json_response_is_passed_on_to_component_factory(self):
        self._request_factory.request.return_value = self.build_mock_response(body='{"foo": "bar"}')
        self._router('')
        self._component_factory.assert_called_once_with({'foo': 'bar'})

    def test_response_from_component_factory_is_passed_to_page_decorator(self):
        expected = sentinel.expected_response
        self._component_factory.return_value = expected
        self._router('')
        self._page_decorator.assert_called_once_with(expected)

    def test_response_from_page_decorator_is_passed_to_view(self):
        expected = sentinel.expected_response
        self._page_decorator.return_value = expected
        self.assertEquals(expected, self._router())

    def build_mock_response(self, body='{}', status=200):
        response = Mock()
        response.status = status
        response.read = Mock(return_value=body)
        return response
