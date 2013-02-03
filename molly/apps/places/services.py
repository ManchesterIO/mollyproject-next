
class PointsOfInterest(object):

    def __init__(self, instance_name, collection, search_index):
        self._instance_name = instance_name
        self._collection = collection.pois
        self._search_index = search_index

    def add_or_update(self, poi):
        existing_poi = self._collection.find_one({'uri': poi.uri})
        if existing_poi:
            poi_dict = poi._asdict()
            poi_dict['_id'] = existing_poi['_id']
            if poi_dict['sources'] != existing_poi['sources']:
                self._collection.update(poi_dict)
                self._add_to_index(poi)
        else:
            self._collection.insert(poi._asdict())
            self._add_to_index(poi)

    def _add_to_index(self, poi):
        self._search_index.add({
            'self': 'http://mollyproject.org/apps/places/point-of-interest',
            'id': '/{instance_name}{uri}'.format(instance_name=self._instance_name, uri=poi.uri),
            'names': [name.name for name in poi.names],
            'descriptions': [description.name for description in poi.descriptions],
            'identifiers': [identifier.value for identifier in poi.identifiers],
            'location': '{lat},{lon}'.format(lat=poi.location.y, lon=poi.location.x) if poi.location else None
        })