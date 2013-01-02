from collections import namedtuple
from shapely import wkt

from molly.apps.common.components import LocalisedName

AccessPoint = namedtuple('AccessPoint', ['names', 'location', 'accessible'])
Identifier = namedtuple('Identifier', ['namespace', 'value'])
OpeningHourRange = namedtuple('OpeningHourRange', [
    'start_date', 'end_date', 'monday_opens', 'monday_closes', 'tuesday_opens', 'tuesday_closes',
    'wednesday_opens', 'wednesday_closes', 'thursday_opens', 'thursday_closes', 'friday_opens', 'friday_closes',
    'saturday_opens', 'saturday_closes', 'sunday_opens', 'sunday_closes'
])
Source = namedtuple('Source', ['url', 'version', 'attribution'])

class PointOfInterest(object):

    def __init__(self, uri=None, names=None, descriptions=None, identifiers=None, address=None, locality=None,
                 telephone_number=None, opening_hours=None, types=None, amenities=None, geography=None, location=None,
                 sources=None):
        self.uri = uri
        self.names = names or []
        self.descriptions = descriptions or []
        self.identifiers = identifiers or []
        self.address = address
        self.locality = locality
        self.telephone_number = telephone_number
        self.opening_hours = opening_hours or []
        self.types = types or []
        self.amenities = amenities or []
        self.geography = geography
        self._location = location
        self.sources = sources or []

    @property
    def location(self):
        if self._location:
            return self._location
        elif self.geography:
            return self.geography.centroid
        else:
            return None

    @location.setter
    def location(self, location):
        self._location = location

    def as_dict(self):
        return {
            'uri': self.uri,
            'names': [name._asdict() for name in self.names],
            'descriptions': [description._asdict() for description in self.descriptions],
            'identifiers': [identifier._asdict() for identifier in self.identifiers],
            'address': self.address,
            'locality': self.locality,
            'telephone_number': self.telephone_number,
            'opening_hours': [opening_hour_range._asdict() for opening_hour_range in self.opening_hours],
            'types': self.types,
            'amenities': self.amenities,
            'geography': wkt.dumps(self.geography) if self.geography else None,
            'location': wkt.dumps(self._location) if self._location else None,
            'sources': [source._asdict() for source in self.sources]
        }

    @classmethod
    def from_dict(cls, data):
        poi = cls()
        poi.uri = data.uri
        poi.names = [LocalisedName(**name) for name in data['names']]
        poi.descriptions = [LocalisedName(**name) for name in data['descriptions']]
        poi.identifiers = [Identifier(**name) for name in data['identifiers']]
        poi.address = data['address']
        poi.locality = data['locality']
        poi.telephone_number = data['telephone_number']
        poi.opening_hours = [OpeningHourRange(**hours) for hours in data['opening_hours']]
        poi.types = data['types']
        poi.amenities = data['amenities']
        poi.geography = wkt.loads(data['geography']) if data['geography'] else None
        poi.location = wkt.loads(data['location']) if data['location'] else None
        poi.sources = [Source(**source) for source in data['sources']]
        return poi


class PointsOfInterest(object):

    def __init__(self, instance_name, collection, search_index):
        self._instance_name = instance_name
        self._collection = collection.pois
        self._search_index = search_index

    def add_or_update(self, poi):
        existing_poi = self._collection.find_one({'uri': poi.uri})
        if existing_poi:
            poi_dict = poi.as_dict()
            poi_dict['_id'] = existing_poi['_id']
            if poi_dict['sources'] != existing_poi['sources']:
                self._collection.update(poi_dict)
                self._add_to_index(poi)
        else:
            self._collection.insert(poi.as_dict())
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
