import geojson
from shapely.geometry import Point
import unittest2 as unittest

from molly.apps.places.models import PointOfInterest


class TestPointOfInterest(unittest.TestCase):

    def test_geography_is_serialised_to_geojson(self):
        poi = PointOfInterest(geography=Point(-2.14, 53.28))
        self.assertEquals(self._point_to_geojson(poi.location), poi._asdict().get('location'))
        self.assertEquals(self._point_to_geojson(poi.geography), poi._asdict().get('geography'))

    def test_geojson_is_deserialised(self):
        point = Point(-2.14, 53.28)

        poi = PointOfInterest.from_dict({
            'geography': self._point_to_geojson(point),
            'location': self._point_to_geojson(point)
        })

        self.assertEquals(point.wkt, poi.location.wkt)
        self.assertEquals(point.wkt, poi.geography.wkt)

    def _point_to_geojson(self, location):
        return geojson.GeoJSONEncoder().default(location)
