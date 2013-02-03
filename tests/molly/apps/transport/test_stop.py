import unittest2 as unittest
from molly.apps.common.components import Source
from molly.apps.transport.stop import Stop, CallingPoint

class StopTest(unittest.TestCase):

    def test_stop_as_dict_includes_appropriate_things(self):
        url = '/test'
        source = Source(url='http://www.example.com', version=1, attribution=None)
        calling_point_url = '/foo'

        stop = Stop()
        stop.url = '/test'
        stop.sources.add(source)
        stop.calling_points.add(calling_point_url)

        self.assertEquals({
            'url': url,
            'sources': [source._asdict()],
            'calling_points': [calling_point_url],
            'identifiers': []
        }, stop.as_dict())


class CallingPointTest(unittest.TestCase):

    def test_stop_as_dict_includes_appropriate_things(self):
        url = '/test'
        source = Source(url='http://www.example.com', version=1, attribution=None)
        parent_url = '/foo'

        calling_point = CallingPoint()
        calling_point.url = '/test'
        calling_point.sources.add(source)
        calling_point.parent_url = parent_url

        self.assertEquals({
            'url': url,
            'sources': [source._asdict()],
            'parent_url': parent_url,
            'identifiers': []
        }, calling_point.as_dict())

    def test_stop_as_dict_includes_appropriate_things_when_no_parent(self):
        url = '/test'
        source = Source(url='http://www.example.com', version=1, attribution=None)

        calling_point = CallingPoint()
        calling_point.url = '/test'
        calling_point.sources = [source]

        self.assertEquals({
            'url': url,
            'sources': [source._asdict()],
            'parent_url': None,
            'identifiers': []
        }, calling_point.as_dict())
