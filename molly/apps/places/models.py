from collections import namedtuple
from flask import request
import geojson
from shapely.geometry import asShape
from flask.ext.babel import lazy_gettext as _

from molly.apps.common.components import LocalisedName, Identifier, Source, Identifiers, LocalisedNames

AccessPoint = namedtuple('AccessPoint', ['names', 'location', 'accessible'])


class PointOfInterest(object):

    def __init__(self, slug=None, names=None, descriptions=None, identifiers=None, address=None, locality=None,
                 telephone_number=None, opening_hours=None, types=None, amenities=None, geography=None, location=None,
                 sources=None):
        self.slug = slug
        self.names = names or LocalisedNames()
        self.descriptions = descriptions or []
        self.identifiers = identifiers or Identifiers()
        self.address = address
        self.locality = locality
        self.telephone_number = telephone_number
        self.opening_hours = opening_hours
        self.types = types or []
        self.amenities = amenities or []
        self.geography = geography
        self._location = location
        self.sources = sources or []

    def name(self):
        for lang in [request.accept_languages.best_match(self.names.language_codes()), None]:
            name = self.names.language(lang)
            if name is not None:
                return name
        else:
            return _('Unnamed Location')

    @property
    def primary_type(self):
        return self.types[0] if self.types else None

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
            'geography': self._point_to_geojson(self.geography),
            'location': self._point_to_geojson(self.location),
            'sources': [source._asdict() for source in self.sources]
        }

    def _point_to_geojson(self, geography):
        return geojson.GeoJSONEncoder().default(geography) if geography else None

    @classmethod
    def from_dict(cls, data):
        poi = cls()
        poi.slug = data.get('slug')
        poi.names = LocalisedNames(LocalisedName(**name) for name in data.get('names', []))
        poi.descriptions = LocalisedNames(LocalisedName(**name) for name in data.get('descriptions', []))
        poi.identifiers = Identifiers(Identifier(**name) for name in data.get('identifiers', []))
        poi.address = data.get('address')
        poi.locality = data.get('locality')
        poi.telephone_number = data.get('telephone_number')
        poi.opening_hours = data.get('opening_hours', [])
        poi.types = data.get('types', [])
        poi.amenities = data.get('amenities', [])
        poi.geography = asShape(data['geography']) if data.get('geography') else None
        poi.location = asShape(data['location']) if data.get('location') else None
        poi.sources = [Source.from_dict(source) for source in data.get('sources', [])]
        return poi


