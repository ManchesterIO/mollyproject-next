from collections import namedtuple
from shapely import wkt

from molly.apps.common.components import LocalisedName, Identifier, Source, Identifiers

AccessPoint = namedtuple('AccessPoint', ['names', 'location', 'accessible'])


class PointOfInterest(object):

    def __init__(self, slug=None, names=None, descriptions=None, identifiers=None, address=None, locality=None,
                 telephone_number=None, opening_hours=None, types=None, amenities=None, geography=None, location=None,
                 sources=None):
        self.slug = slug
        self.names = names or []
        self.descriptions = descriptions or []
        self.identifiers = identifiers or []
        self.address = address
        self.locality = locality
        self.telephone_number = telephone_number
        self.opening_hours = opening_hours
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
            'slug': self.slug,
            'names': [name._asdict() for name in self.names],
            'descriptions': [description._asdict() for description in self.descriptions],
            'identifiers': [identifier._asdict() for identifier in self.identifiers],
            'address': self.address,
            'locality': self.locality,
            'telephone_number': self.telephone_number,
            'opening_hours': self.opening_hours,
            'types': self.types,
            'amenities': self.amenities,
            'geography': wkt.dumps(self.geography) if self.geography else None,
            'location': wkt.dumps(self._location) if self._location else None,
            'sources': [source._asdict() for source in self.sources]
        }

    @classmethod
    def from_dict(cls, data):
        poi = cls()
        poi.slug = data.get('slug')
        poi.names = [LocalisedName(**name) for name in data.get('names', [])]
        poi.descriptions = [LocalisedName(**name) for name in data.get('descriptions', [])]
        poi.identifiers = Identifiers(Identifier(**name) for name in data.get('identifiers', []))
        poi.address = data.get('address')
        poi.locality = data.get('locality')
        poi.telephone_number = data.get('telephone_number')
        poi.opening_hours = data.get('opening_hours', [])
        poi.types = data.get('types', [])
        poi.amenities = data.get('amenities', [])
        poi.geography = wkt.loads(data['geography']) if data.get('geography') else None
        poi.location = wkt.loads(data['location']) if data.get('location') else None
        poi.sources = [Source.from_dict(source) for source in data.get('sources', [])]
        return poi


