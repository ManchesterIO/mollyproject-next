from molly.apps.common.components import Identifiers, Source, Identifier

ATCO_NAMESPACE = 'http://www.naptan.org.uk/AtcoCode'
CIF_DESCRIPTION_NAMESPACE = 'cif:description'
CRS_NAMESPACE = 'http://www.naptan.org.uk/CrsRef'
STANOX_NAMESPACE = 'http://datafeeds.networkrail.co.uk/stanox'
TIPLOC_NAMESPACE = 'http://www.naptan.org.uk/TiplocRef'

class Stop(object):

    def __init__(self):
        self.url = None
        self.sources = set()
        self.calling_points = set()
        self.identifiers = Identifiers()

    @staticmethod
    def from_dict(stop_dict):
        stop = Stop()
        for key, value in stop_dict.iteritems():
            if key == 'sources':
                stop.sources = set(map(lambda source: Source(**source), value))
            elif key == 'url':
                setattr(stop, key, value)
            elif key == 'calling_points':
                stop.calling_points.update(value)
            elif key == 'identifiers':
                stop.identifiers.update(map(lambda identifier: Identifier(**identifier), value))

    def as_dict(self):
        return {
            'url': self.url,
            'calling_points': list(self.calling_points),
            'sources': map(lambda source: source._asdict(), self.sources),
            'identifiers': map(lambda identifier: identifier._asdict(), self.identifiers)
        }


class CallingPoint(object):

    def __init__(self):
        self.url = None
        self.sources = set()
        self.identifiers = Identifiers()
        self.parent_url = None

    @staticmethod
    def from_dict(stop_dict):
        calling_point = CallingPoint
        for key, value in stop_dict.iteritems():
            if key == 'sources':
                calling_point.sources = set(map(lambda source: Source(**source), value))
            elif key == 'identifiers':
                calling_point.identifiers = Identifiers(map(lambda identifier: Identifier(**identifier), value))
            elif key in ('parent_url', 'url'):
                setattr(calling_point, key, value)

    def as_dict(self):
        calling_point_dict = {
            'url': self.url,
            'sources': map(lambda source: source._asdict(), self.sources),
            'identifiers': map(lambda identifier: identifier._asdict(), self.identifiers)
        }

        if hasattr(self, 'parent_url'):
            calling_point_dict['parent_url'] = self.parent_url

        return calling_point_dict
