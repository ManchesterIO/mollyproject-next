from collections import namedtuple

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
