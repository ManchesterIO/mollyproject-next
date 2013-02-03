import geojson
from tch.identifier import Identifiers

NPTG_REGION_CODE_NAMESPACE = "nptg:RegionCode"
NPTG_DISTRICT_CODE_NAMESPACE = "nptg:DistrictCode"
NPTG_LOCALITY_CODE_NAMESPACE = "nptg:LocalityCode"

class Locality(object):

    def __init__(self):
        self._identifiers = Identifiers()
        self.url = None
        self.parent_url = None
        self.geography = None
        self.sources = set()

    @staticmethod
    def from_dict(locality_dict):
        locality = Locality()
        if 'url' in locality_dict: locality.url = locality_dict['url']
        return locality

    @property
    def identifiers(self):
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        self._identifiers = Identifiers(identifiers)

    def as_dict(self):
        serialised = {
            'url': self.url,
            'parent_url': self.parent_url,
            'sources': map(lambda source: source.as_dict(), self.sources),
            'identifiers': map(lambda identifier: identifier.as_dict(), self.identifiers)
        }

        if self.geography:
            encoder = geojson.GeoJSONEncoder()
            serialised['geography'] = encoder.default(self.geography)
            serialised['geography_centroid'] = encoder.default(self.geography.centroid)

        return serialised
