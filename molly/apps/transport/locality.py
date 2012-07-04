import geojson
from tch.identifier import Identifiers

NPTG_REGION_CODE_NAMESPACE = "nptg/RegionCode"
NPTG_DISTRICT_CODE_NAMESPACE = "nptg/DistrictCode"
NPTG_LOCALITY_CODE_NAMESPACE = "nptg/LocalityCode"

class Locality(object):

    @property
    def identifiers(self):
        return getattr(self, '_identifiers', Identifiers())

    @identifiers.setter
    def identifiers(self, identifiers):
        self._identifiers = Identifiers(identifiers)

    def as_dict(self):
        serialised = {}

        if hasattr(self, 'url'):
            serialised['url'] = self.url

        if hasattr(self, 'parent_url'):
            serialised['parent_url'] = self.parent_url

        if hasattr(self, 'geography'):
            encoder = geojson.GeoJSONEncoder()
            serialised['geography'] = encoder.default(self.geography)
            serialised['geography_centroid'] = encoder.default(self.geography.centroid)

        if hasattr(self, 'sources'):
            serialised['sources'] = map(
                lambda source: source.as_dict(),
                self.sources)

        if len(self.identifiers) > 0:
            serialised['identifiers'] = map(
                lambda identifier: identifier.as_dict(),
                self.identifiers)

        return serialised
