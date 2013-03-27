import datetime
import geojson
from shapely.geometry import asShape

from molly.apps.common.components import Identifiers, Source, Identifier

NPTG_REGION_CODE_NAMESPACE = "http://www.naptan.org.uk/RegionCode"
NPTG_DISTRICT_CODE_NAMESPACE = "http://www.naptan.org.uk/NptgDistrictCode"
NPTG_LOCALITY_CODE_NAMESPACE = "http://www.naptan.org.uk/NptgLocalityCode"

ATCO_NAMESPACE = 'http://www.naptan.org.uk/AtcoCode'
CIF_DESCRIPTION_NAMESPACE = 'cif:description'
CRS_NAMESPACE = 'http://www.naptan.org.uk/CrsRef'
STANOX_NAMESPACE = 'http://datafeeds.networkrail.co.uk/stanox'
TIPLOC_NAMESPACE = 'http://www.naptan.org.uk/TiplocRef'


class Locality(object):

    def __init__(self):
        self.names = set()
        self._identifiers = Identifiers()
        self.slug = None
        self.parent_slug = None
        self.geography = None
        self.sources = set()

    @staticmethod
    def from_dict(locality_dict):
        locality = Locality()
        if 'slug' in locality_dict: locality.slug = locality_dict['slug']
        if 'parent_slug' in locality_dict: locality.parent_slug = locality_dict['parent_slug']
        if 'sources' in locality_dict: locality.sources = set(Source(**source) for source in locality_dict['sources'])
        if 'identifiers' in locality_dict:
            locality.identifiers = Identifiers(
                Identifier(**identifier) for identifier in locality_dict['identifiers']
            )
        if 'geography' in locality_dict: locality.geography = asShape(locality_dict['geography'])
        return locality

    @property
    def identifiers(self):
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        self._identifiers = Identifiers(identifiers)

    def _asdict(self):
        serialised = {
            'slug': self.slug,
            'parent_slug': self.parent_slug,
            'sources': map(lambda source: source._asdict(), self.sources),
            'identifiers': map(lambda identifier: identifier._asdict(), self.identifiers)
        }

        if self.geography:
            encoder = geojson.GeoJSONEncoder()
            serialised['geography'] = encoder.default(self.geography)
            serialised['geography_centroid'] = encoder.default(self.geography.centroid)

        return serialised


class Stop(object):

    def __init__(self):
        self.slug = None
        self.sources = set()
        self.calling_points = set()
        self.identifiers = Identifiers()

    @staticmethod
    def from_dict(stop_dict):
        stop = Stop()
        for key, value in stop_dict.iteritems():
            if key == 'sources':
                stop.sources = set(map(lambda source: Source(**source), value))
            elif key == 'slug':
                setattr(stop, key, value)
            elif key == 'calling_points':
                stop.calling_points.update(value)
            elif key == 'identifiers':
                stop.identifiers.update(map(lambda identifier: Identifier(**identifier), value))
        return stop

    def _asdict(self):
        return {
            'slug': self.slug,
            'calling_points': list(self.calling_points),
            'sources': map(lambda source: dict(source._asdict()), self.sources),
            'identifiers': map(lambda identifier: dict(identifier._asdict()), self.identifiers)
        }


class CallingPoint(object):

    def __init__(self):
        self.slug = None
        self.sources = set()
        self.identifiers = Identifiers()
        self.parent_slug = None

    @staticmethod
    def from_dict(stop_dict):
        calling_point = CallingPoint
        for key, value in stop_dict.iteritems():
            if key == 'sources':
                calling_point.sources = set(map(lambda source: Source(**source), value))
            elif key == 'identifiers':
                calling_point.identifiers = Identifiers(map(lambda identifier: Identifier(**identifier), value))
            elif key in ('parent_slug', 'slug'):
                setattr(calling_point, key, value)

    def _asdict(self):
        calling_point_dict = {
            'slug': self.slug,
            'sources': map(lambda source: dict(source._asdict()), self.sources),
            'identifiers': map(lambda identifier: dict(identifier._asdict()), self.identifiers)
        }

        if hasattr(self, 'parent_slug'):
            calling_point_dict['parent_slug'] = self.parent_slug

        return calling_point_dict


class Service(object):
    """
    A high level object to encapsulate an item which a user identifies as an individual service,
    e.g., the 216 bus route or the London-Manchester Pendolino service
    """

    def __init__(self):
        self.name = None
        self.slug = None
        self.mode = None
        self.routes = set()
        self.sources = set()


class Route(object):
    """
    One route which a service operates on - there can be many route variants (e.g., inbound, outbound,
    peak, etc) in a service
    """

    def __init__(self):
        self.slug = None
        self.calling_points = []
        self.service_url = None
        self.headline = None
        self.via = None
        self.sources = set()


class ScheduledTrip(object):
    """
    A scheduled trip is a one particular journey on a route which has timings associated with it
    """

    def __init__(self):
        self.slug = None
        self.route_url = None
        self.calling_points = []
        self.operating_periods = set()
        self.sources = set()


class Call(object):

    # Activities which can be performed at this call
    NORMAL = 'normal' # passengers are picked up and set down
    PASS_THROUGH = 'pass-through' # passes through a point
    OPERATIONAL_STOP = 'operational-stop' # stops for an operational reason (e.g., change of driver)
    PICK_UP_ONLY = 'pick-up-only' # stops to pick up only
    SET_DOWN_ONLY = 'set-down-only' # stops to set down only
    START = 'start' # journey starts here
    FINISH = 'finish' # journey completes here

    def __init__(
            self, point_slug=None, scheduled_arrival_time=None, public_arrival_time=None,
            scheduled_departure_time=None, public_departure_time=None, activity=None
    ):
        self.point_slug = point_slug
        self.scheduled_arrival_time = scheduled_arrival_time
        self.public_arrival_time = public_arrival_time
        self.scheduled_departure_time = scheduled_departure_time
        self.public_departure_time = public_departure_time
        self.activity = activity

    def __eq__(self, other):
        return all(
            map(
                lambda key: getattr(self, key) == getattr(other, key),
                (
                    'point_slug', 'scheduled_arrival_time', 'public_arrival_time',
                    'scheduled_departure_time', 'public_departure_time', 'activity'
                    )
            )
        )

    def __unicode__(self):
        return 'Call(point_slug={point_slug}, scheduled_arrival_time={scheduled_arrival_time}, '\
               'public_arrival_time={public_arrival_time}, scheduled_departure_time={scheduled_departure_time}, '\
               'public_departure_time={public_departure_time}, activity={activity})'.format(
            point_slug=self.point_slug,
            scheduled_arrival_time=self.scheduled_arrival_time,
            public_arrival_time=self.public_arrival_time,
            scheduled_departure_time=self.scheduled_departure_time,
            public_departure_time=self.public_departure_time,
            activity=self.activity
        )

    def __str__(self):
        return str(unicode(self))


class CallTime(datetime.time):
    """
    A time class which handles the fact that some schedules spread over midnight, e.g., a Friday night service
    might actually happen on Saturday morning
    """

    def __init__(self, *args, **kwargs):
        super(CallTime, self).__init__(*args, **kwargs)
        self.next_day = False


class OperationPeriod(object):
    """
    This defines the period which a scheduled trip can run on. A scheduled trip can have multiple applicable periods,
    this captures an individual one. A period is defined by its start date and end date (either or which can be open
    ended and the covered dates are inclusive), Boolean parameters which indicate which days of the week this runs on
    and a set of excluded dates which this period would normally cover but in this case aren't (e.g., bank holidays)
    """

    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.excluded_dates = set()
        self.monday = False
        self.tuesday = False
        self.wednesday = False
        self.thursday = False
        self.friday = False
        self.saturday = False
        self.sunday = False
