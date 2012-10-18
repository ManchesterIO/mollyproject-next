from pprint import pformat

class Component(object):

    def __init__(self, data):
        self._data = data

    def render(self):
        return pformat(self._data)
