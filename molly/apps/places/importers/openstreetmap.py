from datetime import timedelta
from tempfile import NamedTemporaryFile
from urllib2 import urlopen

from celery.schedules import schedule
from imposm.parser import OSMParser
from shapely.geometry import Polygon, LineString, Point

from molly.apps.common.components import Attribution
from molly.config import ConfigError
from molly.apps.places.models import PointOfInterest

ATTRIBUTION = Attribution(
    licence_name='Open Database Licence',
    licence_url='http://www.opendatacommons.org/licenses/odbl',
    attribution_text='OpenStreetMap contributors',
    attribution_url='http://www.openstreetmap.org'
)

OSM_TAGS_TO_TYPES = {
    ('amenity', 'arts_centre'): 'http://mollyproject.org/poi/types/leisure/arts-centre',
    ('amenity', 'bank'): 'http://mollyproject.org/poi/types/retail/bank',
    ('amenity', 'bar'): 'http://mollyproject.org/poi/types/leisure/bar',
    ('amenity', 'bench'): 'http://mollyproject.org/poi/types/leisure/bench',
    ('amenity', 'bicycle_parking'): 'http://mollyproject.org/poi/transport/parking/bicycle',
    ('amenity', 'bicycle_rental'): 'http://mollyproject.org/poi/types/transport/bicycle-rental',
    ('amenity', 'cafe'): 'http://mollyproject.org/poi/types/food/cafe',
    ('amenity', 'cinema'): 'http://mollyproject.org/poi/types/leisure/cinema',
    ('amenity', 'doctors'): 'http://mollyproject.org/poi/types/health/doctors',
    ('amenity', 'fast_food'): 'http://mollyproject.org/poi/types/food/fast-food',
    ('amenity', 'fuel'): 'http://mollyproject.org/poi/types/transport/fuel',
    ('amenity', 'hospital'): 'http://mollyproject.org/poi/types/health/hospital',
    ('amenity', 'library'): 'http://mollyproject.org/poi/types/leisure/library',
    ('amenity', 'marketplace'): 'http://mollyproject.org/poi/types/retail/marketplace',
    ('amenity', 'museum'): 'http://mollyproject.org/poi/types/leisure/museum',
    ('amenity', 'nightclub'): 'http://mollyproject.org/poi/types/leisure/nightclub',
    ('amenity', 'parking'): 'http://mollyproject.org/poi/types/transport/parking/car',
    ('amenity', 'pharmacy'): 'http://mollyproject.org/poi/types/health/pharmacy',
    ('amenity', 'place_of_worship'): 'http://mollyproject.org/poi/types/place-of-worship',
    ('amenity', 'police'): 'http://mollyproject.org/poi/types/police-station',
    ('amenity', 'post_office'): 'http://mollyproject.org/poi/types/retail/post-office',
    ('amenity', 'pub'): 'http://mollyproject.org/poi/types/leisure/pub',
    ('amenity', 'punt_hire'): 'http://mollyproject.org/poi/types/leisure/punt-hire',
    ('amenity', 'restaurant'): 'http://mollyproject.org/poi/types/food/restaurant',
    ('amenity', 'taxi'): 'http://mollyproject.org/poi/types/transport/taxi-rank',
    ('amenity', 'theatre'): 'http://mollyproject.org/poi/types/leisure/theatre',
    ('leisure', 'ice_rink'): 'http://mollyproject.org/poi/types/leisure/ice-rink',
    ('leisure', 'park'): 'http://mollyproject.org/poi/types/leisure/park',
    ('leisure', 'sports_centre'): 'http://mollyproject.org/poi/types/leisure/sports-centre',
    ('leisure', 'swimming_pool'): 'http://mollyproject.org/poi/types/leisure/swimming-pool',
    ('place_of_worship', 'cathedral'): 'http://mollyproject.org/poi/types/place-of-worship/cathedral',
    ('place_of_worship', 'chapel'): 'http://mollyproject.org/poi/types/place-of-worship/chapel',
    ('place_of_worship', 'church'): 'http://mollyproject.org/poi/types/place-of-worship/church',
    ('religion', 'christian'): 'http://mollyproject.org/poi/types/place-of-worship/church',
    ('religion', 'hindu'): 'http://mollyproject.org/poi/types/place-of-worship/mandir',
    ('religion', 'jewish'): 'http://mollyproject.org/poi/types/place-of-worship/synagogue',
    ('religion', 'muslim'): 'http://mollyproject.org/poi/types/place-of-worship/mosque',
    ('sport', 'swimming'): 'http://mollyproject.org/poi/types/leisure/swimming-pool',
    ('tourism', 'information'): 'http://mollyproject.org/poi/types/tourist-information'
}

OSM_TAGS_TO_AMENITIES = {
    ('atm', 'yes'): 'http://mollyproject.org/poi/amenities/atm',
    ('amenity', 'atm'): 'http://mollyproject.org/poi/amenities/atm',
    ('amenity', 'post_box'): 'http://mollyproject.org/poi/amenities/post-box',
    ('amenity', 'recycling'): 'http://mollyproject.org/poi/amenities/recycling',
    ('amenity', 'telephone'): 'http://mollyproject.org/poi/amenities/telephone',
    ('tourism', 'attraction'): 'http://mollyproject.org/poi/amenities/tourist-attraction',
}

class OpenStreetMapImporter(object):
    IMPORTER_NAME = 'openstreetmap'
    IMPORT_SCHEDULE = schedule(run_every=timedelta(weeks=1))

    def __init__(self, config):
        self._parser = OSMParser(
            coords_callback=self.handle_coords,
            nodes_callback=self.handle_nodes,
            ways_callback=self.handle_ways,
            nodes_tag_filter=self.filter_tags,
            ways_tag_filter=self.filter_tags,
        )

        self._interesting_tags = set(OSM_TAGS_TO_AMENITIES.keys() + OSM_TAGS_TO_TYPES.keys())
        self.pois = []
        self._coords = {}

        try:
            self._url = config['url']
        except KeyError:
            raise ConfigError('OpenStreetMap importer must have url config element set')

    def load(self):
        self.pois = []
        self._coords = {}
        with NamedTemporaryFile() as protobuf_file:
            protobuf_file.write(urlopen(self._url).read())
            self._parser.parse_pbf_file(protobuf_file.name)

    def handle_coords(self, coords):
        for id, lat, lon in coords:
            self._coords[id] = (lat, lon)

    def handle_nodes(self, nodes):
        for id, tags, coords in nodes:
            self._add_poi(
                id='N{}'.format(id),
                geography=Point(coords)
            )

    def handle_ways(self, ways):
        for id, tags, nodes in ways:
            if len(tags) > 0:
                if nodes[0] == nodes[-1]:
                    geography_type = Polygon
                else:
                    geography_type = LineString

                self._add_poi(
                    id='W{}'.format(id),
                    geography=geography_type([self._coords[node_id] for node_id in nodes])
                )

    def filter_tags(self, tags):
        if len(set(tags.items()) & self._interesting_tags) == 0:
            for k in tags.keys():
                del tags[k]

    def _add_poi(self, id, geography):
        self.pois.append(PointOfInterest(uri='/osm:{}'.format(id), geography=geography))

Provider = OpenStreetMapImporter
