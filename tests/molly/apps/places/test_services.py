from mock import Mock
from shapely.geometry import Point
import unittest2 as unittest

from molly.apps.common.components import LocalisedName, Identifier, Source, LocalisedNames, Identifiers
from molly.apps.places.models import PointOfInterest
from molly.apps.places.services import PointsOfInterest


class TestPointsOfInterest(unittest.TestCase):

    def setUp(self):
        self._mock_mongo = Mock()
        self._mock_elasticsearch = Mock()
        self._pois = PointsOfInterest('test', self._mock_mongo, self._mock_elasticsearch)
        self._mock_mongo.pois.find_one.return_value = None

    def test_add_adds_to_database(self):
        poi = PointOfInterest()
        self._pois.add_or_update(poi)
        self._mock_mongo.pois.insert.assert_called_once_with(poi._asdict())

    def test_add_indexes(self):
        poi = PointOfInterest()
        poi.slug = 'osm:N12345'
        poi.names = [LocalisedName(name='Test', lang='en')]
        poi.descriptions = [LocalisedName(name='Descriptions', lang='en')]
        poi.geography = Point(-1.6, 54.0)
        poi.identifiers = [Identifier(namespace='foo', value='bar')]

        self._pois.add_or_update(poi)

    def test_add_or_update_checks_for_uri_clashes_before_adding(self):
        self._mock_mongo.pois.find_one.return_value = {
            '_id': 'abcdef', 'sources': [Source(url='http://www.example.com', version=1, attribution='OSM')]
        }
        poi = PointOfInterest(slug='test:test')
        self._pois.add_or_update(poi)
        poi_dict = poi._asdict()
        poi_dict.update({'_id': 'abcdef'})
        self.assertFalse(self._mock_mongo.db.pois.insert.called)
        self._mock_mongo.pois.update.assert_called_once_with({'slug': 'test:test'}, poi_dict)

    def test_add_or_update_does_not_update_if_source_has_not_changed(self):
        self._mock_mongo.pois.find_one.return_value = {
            '_id': 'abcdef',
            'sources': [Source(url='http://www.example.com', version=1, attribution=None)._asdict()]
        }

        poi = PointOfInterest(
            slug='test:test', sources=[Source(url='http://www.example.com', version=1, attribution=None)]
        )
        self._pois.add_or_update(poi)

        self.assertFalse(self._mock_mongo.pois.insert.called)
        self.assertFalse(self._mock_mongo.pois.update.called)

    def test_fetch_by_uri_returns_point_of_interest(self):
        self._mock_mongo.pois.find_one.return_value = {'foo':'bar'}
        self.assertIsInstance(self._pois.select_by_slug('/'), PointOfInterest)

    def test_fetch_by_uri_looks_up_correct_item(self):
        slug = 'foo:bar'
        self._mock_mongo.pois.find_one.return_value = {'locality': 'Eccles'}
        poi = self._pois.select_by_slug(slug)
        self.assertEquals('Eccles', poi.locality)
        self._mock_mongo.pois.find_one.assert_called_once_with({'slug': slug})

    def test_fetch_by_uri_returns_none_when_nothing_found(self):
        self._mock_mongo.pois.find_one.return_value = None
        self.assertIsNone(self._pois.select_by_slug(''))

    def test_slug_is_indexed(self):
        self._mock_mongo.pois.ensure_index.assert_any_call('slug')

    def test_categories_are_indexed(self):
        self._mock_mongo.pois.ensure_index.assert_any_call('categories')

    def test_amenities_are_indexed(self):
        self._mock_mongo.pois.ensure_index.assert_any_call('amenities')

    def test_location_is_indexed(self):
        self._mock_mongo.pois.ensure_index.assert_any_call([('location', '2dsphere')])

    def test_count_nearby_category_returns_0_by_default(self):
        self._setup_results_with_count(0)
        self.assertEquals(0, self._pois.count_nearby_category(Point(-1.6, 54.0), 'http://www.example.com'))

    def test_count_nearby_amenity_returns_0_by_default(self):
        self._setup_results_with_count(0)
        self.assertEquals(0, self._pois.count_nearby_amenity(Point(-1.6, 54.0), 'http://www.example.com'))

    def test_count_from_search_results_for_categories_is_returned(self):
        self._setup_results_with_count(42)
        self.assertEquals(42, self._pois.count_nearby_category(Point(-1.6, 54.0), 'http://www.example.com'))

    def test_count_from_search_results_for_amenities_is_returned(self):
        self._setup_results_with_count(42)
        self.assertEquals(42, self._pois.count_nearby_amenity(Point(-1.6, 54.0), 'http://www.example.com'))

    def test_correct_categories_query_is_supplied_to_mongo(self):
        self._pois.count_nearby_category(Point(-1.6, 54.0), 'http://www.example.com')
        self._mock_mongo.pois.find.assert_called_once_with({
            'location': {'$near': {'$geometry': {'type': 'Point', 'coordinates': (-1.6, 54.0)}}},
            'categories': 'http://www.example.com'
        })

    def test_correct_amenities_query_is_supplied_to_mongo(self):
        self._pois.count_nearby_amenity(Point(-1.6, 54.0), 'http://www.example.com')
        self._mock_mongo.pois.find.assert_called_once_with({
            'location': {'$near': {'$geometry': {'type': 'Point', 'coordinates': (-1.6, 54.0)}}},
            'amenities': 'http://www.example.com'
        })

    def test_maxdistance_parameter_is_provided_when_radius_is(self):
        self._pois.count_nearby_amenity(Point(-1.6, 54.0), 'http://www.example.com', radius=1234)
        self._mock_mongo.pois.find.assert_called_once_with({
            'location': {'$near': {'$geometry': {'type': 'Point', 'coordinates': (-1.6, 54.0)}, '$maxDistance': 1234}},
            'amenities': 'http://www.example.com'
        })

    def test_search_nearby_categories_returns_list_by_default(self):
        self._mock_mongo.pois.find.return_value = []
        self.assertEquals([], self._pois.search_nearby_category(Point(-1.6, 54.0), 'http://www.example.com'))

    def test_search_nearby_amenities_returns_list_by_default(self):
        self._mock_mongo.pois.find.return_value = []
        self.assertEquals([], self._pois.search_nearby_amenity(Point(-1.6, 54.0), 'http://www.example.com'))

    def test_returned_pois_are_returned_as_models_by_category(self):
        self._mock_mongo.pois.find.return_value = [{'slug': 'foo'}]
        points_of_interest = self._pois.search_nearby_category(Point(-1.6, 54.0), 'http://www.example.com')
        self.assertEquals(1, len(points_of_interest))
        self.assertEquals('foo', points_of_interest[0].slug)

    def test_returned_pois_are_returned_as_models_by_amenity(self):
        self._mock_mongo.pois.find.return_value = [{'slug': 'foo'}]
        points_of_interest = self._pois.search_nearby_amenity(Point(-1.6, 54.0), 'http://www.example.com')
        self.assertEquals(1, len(points_of_interest))
        self.assertEquals('foo', points_of_interest[0].slug)

    def test_adding_new_poi_adds_it_to_elasticsearch_index(self):
        poi = PointOfInterest(
            slug='test:test',
            names=LocalisedNames([LocalisedName(name="Hello world", lang="en-gb")]),
            identifiers=Identifiers([Identifier(value="id1", namespace="test")])
        )
        self._pois.add_or_update(poi)
        self._mock_elasticsearch.index.assert_called_once_with(
            'test',
            'poi',
            {
                'names': ['Hello world'],
                'identifiers': ['id1']
            },
            'test:test'
        )

    def test_searching_by_name_constructs_correct_query(self):
        self._mock_elasticsearch.search.return_value = {'hits': {'hits': []}}
        self._mock_mongo.pois.find.return_value = []
        self._pois.search_name("hello world")
        self._mock_elasticsearch.search.assert_called_once_with(
            {
                'query': {
                    'bool': {
                        'should': [
                            {'match': {'names': "hello world"}},
                            {'term': {'identifiers': "hello world"}}
                        ]
                    }
                }
            },
            index='test',
            doc_type='poi'
        )

    def test_search_results_are_fetched_from_mongo(self):
        self._mock_elasticsearch.search.return_value = {
            'hits': {
                'hits': [
                    {'_id': 'test:test1'},
                    {'_id': 'test:test2'}
                ]
            }
        }
        self._mock_mongo.pois.find.return_value = [
            PointOfInterest(slug='test:test2')._asdict(),
            PointOfInterest(slug='test:test1')._asdict()
        ]
        self._pois.search_name("hello world")
        self._mock_mongo.pois.find.assert_called_once_with({"$or": [{"slug": 'test:test1'}, {'slug': 'test:test2'}]})

    def test_pois_are_returned_from_search_by_name(self):
        self._mock_elasticsearch.search.return_value = {
            'hits': {
                'hits': [
                    {'_id': 'test:test1'},
                    {'_id': 'test:test2'}
                ]
            }
        }
        self._mock_mongo.pois.find.return_value = [
            PointOfInterest(slug='test:test2')._asdict(),
            PointOfInterest(slug='test:test1')._asdict()
        ]
        pois = self._pois.search_name("hello world")
        self.assertEquals('test:test1', pois[0].slug)
        self.assertEquals('test:test2', pois[1].slug)

    def test_when_no_results_mongo_is_not_called(self):
        self._mock_elasticsearch.search.return_value = {'hits': {'hits': []}}
        self._pois.search_name("hello world")
        self._mock_mongo.pois.assert_never_called()

    def _setup_results_with_count(self, count):
        mock_result = Mock()
        mock_result.count.return_value = count
        self._mock_mongo.pois.find.return_value = mock_result
