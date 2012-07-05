import unittest
from mock import Mock
from tch.data.locality_service import LocalityMongoDbService
from tch.locality import Locality
from tch.source import Source

class LocalityServiceTest(unittest.TestCase):

    def test_insert_and_merge_posts_inserts_when_new_post(self):
        mock_mongo_connection = self._build_mock_mongo_connection()
        locality = self._insert_and_merge_locality(mock_mongo_connection)
        mock_mongo_connection.localities.insert.assert_called_once_with(locality)

    def test_insert_and_merge_posts_does_not_insert_when_post_exists_and_source_not_changed(self):
        locality = self._build_locality()
        mock_mongo_connection = self._build_mock_mongo_connection(locality)
        locality_service = LocalityMongoDbService(mock_mongo_connection)
        locality_service.insert_and_merge(locality)

        self.assertEqual(0, mock_mongo_connection.localities.insert.call_count)

    def test_insert_and_merge_posts_does_insert_when_post_exists_and_source_not_in_sources(self):
        db_locality = self._build_locality()
        db_locality.sources = []
        mock_mongo_connection = self._build_mock_mongo_connection(db_locality)

        self._insert_and_merge_locality(mock_mongo_connection)

        self.assertEqual(1, mock_mongo_connection.localities.insert.call_count)

    def test_insert_and_merge_posts_maintains_other_sources_when_merging(self):
        db_locality = self._build_locality()
        db_locality.sources[0].url = 'othersource'
        other_source = db_locality.sources[0]
        mock_mongo_connection = self._build_mock_mongo_connection(db_locality)

        self._insert_and_merge_locality(mock_mongo_connection)

        self.assertIn(other_source, mock_mongo_connection.localities.insert.call_args[0][0].sources)

    def test_insert_and_merge_posts_removes_old_versions_of_source_when_merging(self):
        mock_mongo_connection, old_source = self._build_mock_mongo_connection_with_old_source()

        self._insert_and_merge_locality(mock_mongo_connection)

        self.assertNotIn(old_source, self._get_inserted_locality(mock_mongo_connection).sources)

    def test_insert_and_merge_includes_new_source_when_merging(self):
        mock_mongo_connection, old_source = self._build_mock_mongo_connection_with_old_source()
        locality = self._insert_and_merge_locality(mock_mongo_connection)
        self.assertIn(locality.sources[0], self._get_inserted_locality(mock_mongo_connection).sources)

    def _insert_and_merge_locality(self, mock_mongo_connection):
        locality_service = LocalityMongoDbService(mock_mongo_connection)
        locality = self._build_locality()
        locality_service.insert_and_merge(locality)
        return locality

    def _get_inserted_locality(self, mock_mongo_connection):
        return mock_mongo_connection.localities.insert.call_args[0][0]

    def _build_locality(self):
        locality = Locality()
        locality.url = '/test'
        locality.sources = [Source(url='http://www.example.com', version=2)]
        return locality

    def _build_mock_mongo_connection(self, return_locality=None):
        mock_mongo_connection = Mock()
        mock_mongo_connection.localities = Mock()
        mock_mongo_connection.localities.insert = Mock()
        mock_mongo_connection.localities.find_one = Mock(return_value=return_locality)
        return mock_mongo_connection

    def _build_mock_mongo_connection_with_old_source(self):
        db_locality = self._build_locality()
        db_locality.sources[0].version = 1
        old_source = db_locality.sources[0]
        mock_mongo_connection = self._build_mock_mongo_connection(db_locality)
        return mock_mongo_connection, old_source
