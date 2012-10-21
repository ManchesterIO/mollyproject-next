import json
from werkzeug.exceptions import NotFound, ServiceUnavailable, BadGateway

class Router(object):

    def __init__(self, request_factory, component_factory, page_decorator_factory):
        self._request_factory = request_factory
        self._component_factory = component_factory
        self._page_decorator_factory = page_decorator_factory

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
                page_decorator = self._page_decorator_factory.get_decorator(path)
                return page_decorator(self._component_factory(response))
        elif response.status == 404:
            return NotFound()
        else:
            raise RoutingException(response)


class RoutingException(Exception):
    """
    Raised when the underlying Molly service returns something unexpected
    """

    def __init__(self, response):
        self.response = response
