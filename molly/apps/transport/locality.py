import geojson
from tch.identifier import IdentifierList

NPTG_REGION_CODE_NAMESPACE = "nptg/RegionCode"

class Locality(object):

    @property
    def identifiers(self):
        return IdentifierList(getattr(self, '_identifiers', []))

    @identifiers.setter
    def identifiers(self, identifiers):
        self._identifiers = identifiers

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
