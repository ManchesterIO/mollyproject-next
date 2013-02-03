import unittest2 as unittest
from mock import Mock
from shapely.geometry.point import Point
from tch.data.locality_service import LocalityService
from tch.identifier import Identifier
from tch.locality import Locality
from tch.source import Source


class LocalityServiceTest(unittest.TestCase):

    URL = '/test'
    PARENT_URL = '/parent_test'
    IDENTIFIER = Identifier(namespace='test', value='test')

    def test_insert_and_merge_posts_inserts_when_new_post(self):
        mock_connection = self._build_mock_connection()
        locality = self._insert_and_merge_locality(mock_connection)
        mock_connection.insert.assert_called_once_with(locality)

    def test_insert_and_merge_looks_up_by_url(self):
        mock_connection = self._build_mock_connection()
        self._insert_and_merge_locality(mock_connection)
        mock_connection.select_by_url.assert_called_once_with(self.URL)

    def test_insert_and_merge_posts_does_not_insert_when_post_exists_and_source_not_changed(self):
        locality = self._build_locality()
        mock_connection = self._build_mock_connection(locality)
        locality_service = LocalityService(mock_connection)
        locality_service.insert_and_merge(locality)

        self.assertEqual(0, mock_connection.insert.call_count)

    def test_insert_and_merge_posts_does_insert_when_post_exists_and_source_not_in_sources(self):
        db_locality = self._build_locality()
        db_locality.sources = set()
        mock_connection = self._build_mock_connection(db_locality)

        self._insert_and_merge_locality(mock_connection)

        self.assertEqual(1, mock_connection.insert.call_count)

    def test_insert_and_merge_posts_maintains_other_sources_when_merging(self):
        db_locality = self._build_locality()
        other_source = Source(url='http://www.othersource.com', version=2)
        db_locality.sources = {other_source}
        mock_connection = self._build_mock_connection(db_locality)

        self._insert_and_merge_locality(mock_connection)

        self.assertIn(other_source, mock_connection.insert.call_args[0][0].sources)

    def test_insert_and_merge_posts_removes_old_versions_of_source_when_merging(self):
        mock_connection, old_source = self._build_mock_connection_with_old_source()

        self._insert_and_merge_locality(mock_connection)

        self.assertNotIn(old_source, self._get_inserted_locality(mock_connection).sources)

    def test_insert_and_merge_includes_new_source_when_merging(self):
        mock_connection, old_source = self._build_mock_connection_with_old_source()
        locality = self._insert_and_merge_locality(mock_connection)
        self.assertIn(locality.sources.pop(), self._get_inserted_locality(mock_connection).sources)

    def test_insert_and_merge_replaces_parent_url(self):
        expected_url = "/new_test"
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        new_locality.parent_url = expected_url

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual(expected_url, self._get_inserted_locality(mock_connection).parent_url)

    def test_insert_and_merge_leaves_parent_url_when_unset(self):
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        delattr(new_locality, 'parent_url')

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual("/parent_test", self._get_inserted_locality(mock_connection).parent_url)

    def test_insert_and_merge_replaces_geography(self):
        expected_geography = Point(-1, -1)
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        new_locality.geography = expected_geography

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual(expected_geography.xy, self._get_inserted_locality(mock_connection).geography.xy)

    def test_insert_and_merge_leaves_parent_geography_when_unset(self):
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        delattr(new_locality, 'geography')

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual(Point(0, 0).xy, self._get_inserted_locality(mock_connection).geography.xy)

    def test_insert_and_merge_adds_new_identifiers(self):
        old_locality, old_source = self._build_old_locality()
        new_locality, identifier = self._build_locality_with_different_identifier()

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertIn(identifier, self._get_inserted_locality(mock_connection).identifiers)

    def test_insert_and_merge_retains_old_identifiers(self):
        old_locality, old_source = self._build_old_locality()
        new_locality, identifier = self._build_locality_with_different_identifier()

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertIn(self.IDENTIFIER, self._get_inserted_locality(mock_connection).identifiers)

    def _insert_and_merge_with(self, new_locality, old_locality):
        mock_connection = self._build_mock_connection(old_locality)
        locality_service = LocalityService(mock_connection)
        locality_service.insert_and_merge(new_locality)
        return mock_connection

    def _insert_and_merge_locality(self, mock_connection):
        locality_service = LocalityService(mock_connection)
        locality = self._build_locality()
        locality_service.insert_and_merge(locality)
        return locality

    def _get_inserted_locality(self, mock_connection):
        return mock_connection.insert.call_args[0][0]

    def _build_locality(self):
        locality = Locality()
        locality.url = self.URL
        locality.parent_url = self.PARENT_URL
        locality.sources = {Source(url='http://www.example.com', version=2)}
        locality.geography = Point(0, 0)
        locality.identifiers = [self.IDENTIFIER]
        return locality

    def _build_old_locality(self):
        old_locality = self._build_locality()
        source = Source(url='http://www.example.com', version=0)
        old_locality.sources = {source}
        return old_locality, source

    def _build_locality_with_different_identifier(self):
        new_locality = self._build_locality()
        identifier = Identifier(namespace="new_test", value="new_value")
        new_locality.identifiers = [identifier]
        return new_locality, identifier

    def _build_mock_connection(self, return_locality=None):
        mock_connection = Mock()
        mock_connection.select_by_url = Mock(return_value=return_locality)
        return mock_connection

    def _build_mock_connection_with_old_source(self):
        db_locality, old_source = self._build_old_locality()
        mock_mongo_connection = self._build_mock_connection(db_locality)
        return mock_mongo_connection, old_source
