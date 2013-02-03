from collections import namedtuple
from shapely import wkt

from molly.apps.common.components import LocalisedName, Identifier, Source, Identifiers

AccessPoint = namedtuple('AccessPoint', ['names', 'location', 'accessible'])
OpeningHourRange = namedtuple('OpeningHourRange', [
    'start_date', 'end_date', 'monday_opens', 'monday_closes', 'tuesday_opens', 'tuesday_closes',
    'wednesday_opens', 'wednesday_closes', 'thursday_opens', 'thursday_closes', 'friday_opens', 'friday_closes',
    'saturday_opens', 'saturday_closes', 'sunday_opens', 'sunday_closes'
])

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

    def _asdict(self):
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
        poi.identifiers = Identifiers(Identifier(**name) for name in data['identifiers'])
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
