import json
from werkzeug.exceptions import NotFound, ServiceUnavailable, BadGateway

class Router(object):

    def __init__(self, request_factory, component_factory, page_decorator):
        self._request_factory = request_factory
        self._component_factory = component_factory
        self._page_decorator = page_decorator

    def __call__(self, path=''):
        try:
            response = self._request_factory.request('/{}'.format(path))
        except self._request_factory.RequestException:
            return ServiceUnavailable()

        if response.status == 200:
            try:
                response = json.load(response)
            except (TypeError, ValueError):
                return BadGateway()
            else:
                return self._page_decorator(self._component_factory(response))
        elif response.status == 404:
            return NotFound()
