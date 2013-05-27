from molly.apps.places.models import PointOfInterest


class PointsOfInterest(object):

    def __init__(self, instance_name, connection):
        self._instance_name = instance_name
        self._collection = connection.pois

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
        else:
            self._collection.insert(poi._asdict())
