from mock import Mock
import unittest2 as unittest

from molly.apps.transport.data.mongo.localities import LocalityMongoDb
from molly.apps.transport.locality import Locality

class LocalityMongoDbTest(unittest.TestCase):

    URL = "/test"

    def test_fetching_by_url_returns_correct_object(self):
        locality_mongo_db, mock_connection = self._build_db_with_mock_connection({'url': self.URL})
        locality = locality_mongo_db.select_by_url(self.URL)
        self.assertEqual(self.URL, locality.url)

    def test_selecting_by_url_returns_none(self):
        locality_mongo_db, mock_connection = self._build_db_with_mock_connection(None)
        self.assertEquals(None, locality_mongo_db.select_by_url(self.URL))

    def test_inserting_inserts_into_collection(self):
        locality_mongo_db, mock_connection = self._build_db_with_mock_connection(None)
        locality = self._build_locality()

        locality_mongo_db.insert(locality)

        mock_connection.save.assert_called_once_with(locality.as_dict())

    def test_inserting_inserts_into_collection_with_same_id(self):
        expected_id = 12345
        locality_mongo_db, mock_connection = self._build_db_with_mock_connection({
            '_id': expected_id,
            'url': self.URL
        })
        locality = self._build_locality()

        locality_mongo_db.insert(locality)

        self.assertEqual(expected_id, mock_connection.save.call_args[0][0]['_id'])

    def test_url_is_indexed(self):
        locality_mongo_db, mock_connection = self._build_db_with_mock_connection(None)
        mock_connection.ensure_index.assert_called_once_with('url')

    def _build_db_with_mock_connection(self, result):
        mock_connection = Mock()
        mock_connection.find_one = Mock(return_value=result)
        return LocalityMongoDb(mock_connection), mock_connection

    def _build_locality(self):
        locality = Locality()
        locality.url = self.URL
        return locality

