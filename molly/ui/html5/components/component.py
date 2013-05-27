from urlparse import urlparse


class Component(object):

    _CSS = frozenset()

    def __init__(self, data, component_factory):
        self._data = data
        self._component_factory = component_factory
        self._css = set(self._CSS)

    @property
    def title(self):
        raise NotImplementedError()

    @property
    def href(self):
        return urlparse(self._data.get('href')).path

    @property
    def css(self):
        return list(self._css)

    def render_header(self):
        return ''

    def render(self):
        raise NotImplementedError()

    def _add_css(self, css):
        self._css.add(css)

    def _load_component(self, component_data):
        component = self._component_factory(component_data)
        for css in component.css: self._add_css(css)
        return component
