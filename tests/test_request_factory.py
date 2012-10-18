import socket
from mock import Mock
import unittest2 as unittest
from molly.ui.html5 import request_factory

class HttpRequestFactoryTest(unittest.TestCase):

    def setUp(self):
        self._factory = request_factory.HttpRequestFactory('localhost', 8000)
        self._mock_http_connection = Mock()
        request_factory.HTTPConnection = self._mock_http_connection
        self._mock_connection = Mock()
        self._mock_http_connection.return_value = self._mock_connection

    def test_socket_error_raises_service_error(self):
        self._mock_connection.request.side_effect = socket.error

        self.assertRaises(self._factory.RequestException, self._factory.request, '/')

    def test_accept_json_header_is_set(self):
        self._factory.request('/')

        self.assertEquals(
            {'Accept': 'application/json'},
            self._mock_connection.request.call_args[1]['headers']
        )

