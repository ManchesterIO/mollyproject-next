import logging
import geojson
from molly.apps.places.models import PointOfInterest

LOGGER = logging.getLogger(__name__)


class PointsOfInterest(object):

    def __init__(self, instance_name, connection):
        self._instance_name = instance_name
        self._collection = connection.pois
        self._collection.ensure_index('slug')
        self._collection.ensure_index({'location': '2dsphere'}.items())
        self._collection.ensure_index('categories')
        self._collection.ensure_index('amenities')

    def select_by_slug(self, slug):
        poi_dict = self._collection.find_one({'slug': slug})
        return PointOfInterest.from_dict(poi_dict) if poi_dict else None

    def add_or_update(self, poi):
        existing_poi = self._collection.find_one({'slug': poi.slug})
        if existing_poi:
            poi_dict = poi._asdict()
            poi_dict['_id'] = existing_poi['_id']
            if poi_dict['sources'] != existing_poi['sources']:
                self._collection.update({'slug': poi.slug}, poi_dict)
                LOGGER.info("Updating existing POI %s", poi.slug)
            else:
                LOGGER.info("POI %s is no different to one already in database", poi.slug)
        else:
            self._collection.insert(poi._asdict())
            LOGGER.info("Inserting new POI %s", poi.slug)

    def count_nearby_category(self, point, category, radius=None):
        return self._count_nearby(point, 'categories', category, radius)

    def count_nearby_amenity(self, point, amenity, radius=None):
        return self._count_nearby(point, 'amenities', amenity, radius)

    def search_nearby_category(self, point, category, radius=None):
        return map(PointOfInterest.from_dict, self._search_nearby(point, 'categories', category, radius))

    def search_nearby_amenity(self, point, amenity, radius=None):
        return map(PointOfInterest.from_dict, self._search_nearby(point, 'amenities', amenity, radius))

    def _count_nearby(self, point, facet, uri, radius):
        return self._search_nearby(point, facet, uri, radius).count()

    def _search_nearby(self, point, facet, uri, radius):
        query = {
            'location': {'$near': {'$geometry': geojson.GeoJSONEncoder().default(point)}},
            facet: uri
        }
        if radius is not None:
            query['location']['$near']['$maxDistance'] = radius
        return self._collection.find(query)
