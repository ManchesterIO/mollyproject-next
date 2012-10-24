from tch.source import Source

class Stop(object):

    def __init__(self):
        self.calling_points = set()

    @staticmethod
    def from_dict(stop_dict):
        stop = Stop()
        for key, value in stop_dict.iteritems():
            if key == 'sources':
                stop.sources = map(lambda source: Source(**source), value)
            elif key == 'url':
                setattr(stop, key, value)
            elif key == 'calling_points':
                stop.calling_points.update(value)

    def as_dict(self):
        return {
            'url': self.url,
            'calling_points': list(self.calling_points),
            'sources': map(lambda source: source.as_dict(), self.sources)
        }


class CallingPoint(object):

    @staticmethod
    def from_dict(stop_dict):
        calling_point = CallingPoint
        for key, value in stop_dict.iteritems():
            if key == 'sources':
                calling_point.sources = map(lambda source: Source(**source), value)
            elif key in ('parent_url', 'url'):
                setattr(calling_point, key, value)

    def as_dict(self):
        calling_point_dict = {
            'url': self.url,
            'sources': map(lambda source: source.as_dict(), self.sources)
        }

        if hasattr(self, 'parent_url'):
            calling_point_dict['parent_url'] = self.parent_url

        return calling_point_dict
