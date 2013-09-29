from urllib import unquote
from molly.ui.html5.filters import ui_url


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
        return ui_url(unquote(self._data.get('href')))

    @property
    def css(self):
        return list(self._css)

    def render_header(self):
        return ''

    def render(self, **kwargs):
        raise NotImplementedError()

    def _add_css(self, css):
        self._css.add(css)

    def _load_component(self, component_data):
        component = self._component_factory(component_data)
        for css in component.css: self._add_css(css)
        return component
