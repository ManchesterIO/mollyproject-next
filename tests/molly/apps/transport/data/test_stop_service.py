from mock import Mock
import unittest2 as unittest
from molly.apps.common.components import Source
from molly.apps.transport.data.stop_service import StopService
from molly.apps.transport.models import Stop

class StopServiceTest(unittest.TestCase):

    _URL = '/gb/ECCLES'

    def setUp(self):
        self._mock_connection = Mock()
        self._mock_connection.insert = Mock()
        self._mock_connection.select_by_url = Mock(return_value=None)
        self._stop_service = StopService(self._mock_connection)

    def test_insert_and_merge_inserts_when_new(self):
        stop = self._build_stop()
        self._stop_service.insert_and_merge(stop)
        self._mock_connection.insert.assert_called_once_with(stop)

    def test_insert_and_merge_does_not_insert_when_stop_exists_and_source_not_changed(self):
        stop = self._build_stop()
        self._mock_connection.select_by_url.return_value = stop

        self._stop_service.insert_and_merge(stop)

        self.assertEqual(0, self._mock_connection.insert.call_count)
        self._mock_connection.select_by_url.assert_called_once_with(stop.url, filter_by_type=Stop)

    def test_insert_and_merge_does_insert_when_stop_exists_and_source_changed(self):
        old_stop = self._build_stop()
        self._mock_connection.select_by_url.return_value = old_stop
        new_stop = self._build_stop()
        new_source = Source(url='http://www.example.com', version=2, attribution=None)
        new_stop.sources = {new_source}

        self._stop_service.insert_and_merge(new_stop)

        inserted_stop = self._mock_connection.insert.call_args[0][0]
        self.assertIn(new_source, inserted_stop.sources)

    def _build_stop(self):
        stop = Stop()
        stop.url = self._URL
        stop.sources = {Source(url='http://www.example.com', version=1, attribution=None)}
        return stop
