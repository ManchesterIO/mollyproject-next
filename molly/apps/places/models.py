from collections import namedtuple
from molly.apps.common.components import Attribution

AccessPoint = namedtuple('AccessPoint', ['names', 'location', 'accessible'])
Identifier = namedtuple('Identifier', ['namespace', 'value'])
OpeningHourRange = namedtuple('OpeningHourRange', [
    'start_date', 'end_date', 'opens', 'closes', 'applies_monday', 'applies_tuesday', 'applies_wednesday',
    'applies_thursday', 'applies_friday', 'applies_saturday', 'applies_sunday', 'applies_public_holidays'
])
Source = namedtuple('Source', ['url', 'version', 'attribution'])

ATTRIBUTION = Attribution(
    licence_name='Open Database Licence',
    licence_url='http://www.opendatacommons.org/licenses/odbl',
    attribution_text='OpenStreetMap contributors',
    attribution_url='http://www.openstreetmap.org'
)

class PointOfInterest(object):

    def __init__(self, uri=None, names=[], descriptions=[], identifiers=[], address=None, locality=None,
                 telephone_number=None, opening_hours=[], types=[], primary_type=None, amenities=[],
                 geography=None, location=None, sources=[]):
        self.uri = uri
        self.names = names
        self.descriptions = descriptions
        self.identifiers = identifiers
        self.address = address
        self.locality = locality
        self.telephone_number = telephone_number
        self.opening_hours = opening_hours
        self.types = types
        self.primary_type = primary_type
        self.amenities = amenities
        self.geography = geography
        self._location = location
        self.sources = sources

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
