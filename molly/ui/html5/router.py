import json
from werkzeug.exceptions import NotFound, ServiceUnavailable, BadGateway

class Router(object):

    def __init__(self, request_factory, component_factory, page_decorator_factory, statsd):
        self._request_factory = request_factory
        self._component_factory = component_factory
        self._page_decorator_factory = page_decorator_factory
        self._statsd = statsd

    def __call__(self, path=''):
        try:
            with self._statsd.timer('molly.ui.html5.api_request_time'):
                response = self._request_factory.request('/{}'.format(path))
        except self._request_factory.RequestException:
            self._statsd.incr('molly.ui.html5.api_unavailable')
            return ServiceUnavailable()

        if response.status == 200:
            try:
                response = json.load(response)
            except (TypeError, ValueError):
                self._statsd.incr('molly.ui.html5.api_bad_response')
                return BadGateway()
            else:
                self._statsd.incr('molly.ui.html5.api_success')
                try:
                    with self._statsd.timer('molly.ui.html5.page_build_time'):
                        page_decorator = self._page_decorator_factory.get_decorator(path)
                        return page_decorator(self._component_factory(response))
                except Exception:
                    self._statsd.incr('molly.ui.html5.page_build_error')
                    raise
        elif response.status == 404:
            self._statsd.incr('molly.ui.html5.api_404')
            return NotFound()
        else:
            self._statsd.incr('molly.ui.html5.api_error')
            raise RoutingException(response)


class RoutingException(Exception):
    """
    Raised when the underlying Molly service returns something unexpected
    """

    def __init__(self, response):
        self.response = response
