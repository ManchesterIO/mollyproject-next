import unittest2 as unittest
from tch.source import Source
from tch.stop import Stop, CallingPoint

class StopTest(unittest.TestCase):

    def test_stop_as_dict_includes_appropriate_things(self):
        url = '/test'
        source = Source()
        calling_point_url = '/foo'

        stop = Stop()
        stop.url = '/test'
        stop.sources = [source]
        stop.calling_points.add(calling_point_url)

        self.assertEquals({
            'url': url,
            'sources': [source.as_dict()],
            'calling_points': [calling_point_url]
        }, stop.as_dict())


class CallingPointTest(unittest.TestCase):

    def test_stop_as_dict_includes_appropriate_things(self):
        url = '/test'
        source = Source()
        parent_url = '/foo'

        calling_point = CallingPoint()
        calling_point.url = '/test'
        calling_point.sources = [source]
        calling_point.parent_url = parent_url

        self.assertEquals({
            'url': url,
            'sources': [source.as_dict()],
            'parent_url': parent_url
        }, calling_point.as_dict())

    def test_stop_as_dict_includes_appropriate_things_when_no_parent(self):
        url = '/test'
        source = Source()
        parent_url = '/foo'

        calling_point = CallingPoint()
        calling_point.url = '/test'
        calling_point.sources = [source]

        self.assertEquals({
            'url': url,
            'sources': [source.as_dict()]
        }, calling_point.as_dict())
