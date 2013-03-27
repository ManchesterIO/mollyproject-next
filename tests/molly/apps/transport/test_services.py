import unittest2 as unittest
from mock import Mock
from shapely.geometry.point import Point

from molly.apps.common.components import Identifier, Source
from molly.apps.transport.services import StopService, LocalityService
from molly.apps.transport.models import Locality, Stop


class LocalityServiceTest(unittest.TestCase):

    SLUG = '/test'
    PARENT_URL = '/parent_test'
    IDENTIFIER = Identifier(namespace='test', value='test')

    def test_insert_and_merge_posts_inserts_when_new_post(self):
        mock_connection = self._build_mock_connection()
        locality = self._insert_and_merge_locality(mock_connection)
        mock_connection.localities.save.assert_called_once_with(locality._asdict())

    def test_insert_and_merge_looks_up_by_url(self):
        mock_connection = self._build_mock_connection()
        self._insert_and_merge_locality(mock_connection)
        mock_connection.localities.find_one.assert_called_once_with({'slug': self.SLUG})

    def test_insert_and_merge_posts_does_not_insert_when_post_exists_and_source_not_changed(self):
        locality = self._build_locality()
        mock_connection = self._build_mock_connection(locality)
        locality_service = LocalityService(mock_connection)
        locality_service.insert_and_merge(locality)

        self.assertEqual(0, mock_connection.localities.save.call_count)

    def test_insert_and_merge_posts_does_insert_when_post_exists_and_source_not_in_sources(self):
        db_locality = self._build_locality()
        db_locality.sources = set()
        mock_connection = self._build_mock_connection(db_locality)

        self._insert_and_merge_locality(mock_connection)

        self.assertEqual(1, mock_connection.localities.save.call_count)

    def test_insert_and_merge_posts_maintains_other_sources_when_merging(self):
        db_locality = self._build_locality()
        other_source = Source(url='http://www.othersource.com', version=2, attribution=None)
        db_locality.sources = {other_source}
        mock_connection = self._build_mock_connection(db_locality)

        self._insert_and_merge_locality(mock_connection)

        self.assertIn(other_source._asdict(), mock_connection.localities.save.call_args[0][0]['sources'])

    def test_insert_and_merge_posts_removes_old_versions_of_source_when_merging(self):
        mock_connection, old_source = self._build_mock_connection_with_old_source()

        self._insert_and_merge_locality(mock_connection)

        self.assertNotIn(old_source._asdict(), self._get_inserted_locality(mock_connection)['sources'])

    def test_insert_and_merge_includes_new_source_when_merging(self):
        mock_connection, old_source = self._build_mock_connection_with_old_source()
        locality = self._insert_and_merge_locality(mock_connection)
        self.assertIn(locality.sources.pop()._asdict(), self._get_inserted_locality(mock_connection)['sources'])

    def test_insert_and_merge_replaces_parent_url(self):
        expected_slug = "/new_test"
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        new_locality.parent_slug = expected_slug

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual(expected_slug, self._get_inserted_locality(mock_connection)['parent_slug'])

    def test_insert_and_merge_leaves_parent_slug_when_unset(self):
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        delattr(new_locality, 'parent_slug')

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual("/parent_test", self._get_inserted_locality(mock_connection)['parent_slug'])

    def test_insert_and_merge_replaces_geography(self):
        expected_geography = Point(-1, -1)
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        new_locality.geography = expected_geography

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual(
            new_locality._asdict().get('geography'),
            self._get_inserted_locality(mock_connection)['geography']
        )

    def test_insert_and_merge_leaves_parent_geography_when_unset(self):
        old_locality, old_source = self._build_old_locality()
        new_locality = self._build_locality()
        delattr(new_locality, 'geography')

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual(old_locality._asdict().get('geography'), self._get_inserted_locality(mock_connection)['geography'])

    def test_insert_and_merge_adds_new_identifiers(self):
        old_locality, old_source = self._build_old_locality()
        new_locality, identifier = self._build_locality_with_different_identifier()

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertIn(identifier._asdict(), self._get_inserted_locality(mock_connection)['identifiers'])

    def test_insert_and_merge_retains_old_identifiers(self):
        old_locality, old_source = self._build_old_locality()
        new_locality, identifier = self._build_locality_with_different_identifier()

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertIn(self.IDENTIFIER._asdict(), self._get_inserted_locality(mock_connection)['identifiers'])

    def test_slug_is_indexed(self):
        mock_connection = self._build_mock_connection()
        LocalityService(mock_connection)
        mock_connection.localities.ensure_index.assert_called_once_with('slug')


    def test_inserting_inserts_into_collection_with_same_id(self):
        new_locality = self._build_locality()
        old_locality, source = self._build_old_locality()

        mock_connection = self._insert_and_merge_with(new_locality, old_locality)

        self.assertEqual('12345', mock_connection.localities.save.call_args[0][0]['_id'])

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
        return mock_connection.localities.save.call_args[0][0]

    def _build_locality(self):
        locality = Locality()
        locality.slug = self.SLUG
        locality.parent_slug = self.PARENT_URL
        locality.sources = {Source(url='http://www.example.com', version=2, attribution=None)}
        locality.geography = Point(0, 0)
        locality.identifiers = [self.IDENTIFIER]
        return locality

    def _build_old_locality(self):
        old_locality = self._build_locality()
        source = Source(url='http://www.example.com', version=0, attribution=None)
        old_locality.sources = {source}
        return old_locality, source

    def _build_locality_with_different_identifier(self):
        new_locality = self._build_locality()
        identifier = Identifier(namespace="new_test", value="new_value")
        new_locality.identifiers = [identifier]
        return new_locality, identifier

    def _build_mock_connection(self, return_locality=None):
        mock_connection = Mock()
        if return_locality:
            return_locality_dict = return_locality._asdict()
            return_locality_dict['_id'] = '12345'
        else:
            return_locality_dict = None
        mock_connection.localities.find_one = Mock(return_value=return_locality_dict)
        return mock_connection

    def _build_mock_connection_with_old_source(self):
        db_locality, old_source = self._build_old_locality()
        mock_mongo_connection = self._build_mock_connection(db_locality)
        return mock_mongo_connection, old_source


class StopServiceTest(unittest.TestCase):

    _URL = '/gb/ECCLES'

    def setUp(self):
        self._mock_connection = Mock()
        self._mock_connection.stops.find_one = Mock(return_value=None)
        self._stop_service = StopService(self._mock_connection)

    def test_insert_and_merge_inserts_when_new(self):
        stop = self._build_stop()
        self._stop_service.insert_and_merge(stop)
        stop_dict = stop._asdict()
        stop_dict['_type'] = 'stop'
        self._mock_connection.stops.save.assert_called_once_with(stop_dict)

    def test_insert_and_merge_does_not_insert_when_stop_exists_and_source_not_changed(self):
        stop = self._build_stop()
        self._set_return_stop(stop)

        self._stop_service.insert_and_merge(stop)

        self.assertEqual(0, self._mock_connection.save.call_count)
        self._mock_connection.stops.find_one.assert_called_once_with({'slug': stop.slug, '_type': 'stop'})

    def test_insert_and_merge_does_insert_when_stop_exists_and_source_changed(self):
        old_stop = self._build_stop()
        self._set_return_stop(old_stop)
        new_stop = self._build_stop()
        new_source = Source(url='http://www.example.com', version=2, attribution=None)
        new_stop.sources = {new_source}

        self._stop_service.insert_and_merge(new_stop)

        inserted_stop = self._mock_connection.stops.save.call_args[0][0]
        self.assertIn(new_source._asdict(), inserted_stop['sources'])

    def _build_stop(self):
        stop = Stop()
        stop.slug = self._URL
        stop.sources = {Source(url='http://www.example.com', version=1, attribution=None)}
        return stop

    def _set_return_stop(self, stop):
        stop_dict = stop._asdict()
        stop_dict['_id'] = '12345'
        stop_dict['_type'] = 'stop'
        self._mock_connection.stops.find_one.return_value = stop_dict
        self._mock_connection.stops.find.return_value = [stop_dict]
