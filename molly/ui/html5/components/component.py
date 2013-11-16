from urllib import unquote
from molly.ui.html5.filters import ui_url


class Component(object):

    def __init__(self, data, component_factory):
        self._data = data
        self._component_factory = component_factory

    @property
    def title(self):
        raise NotImplementedError()

    @property
    def href(self):
        return ui_url(unquote(self._data.get('href')))

    def render_header(self):
        return ''

    def render(self, **kwargs):
        return ''

    def _load_component(self, component_data):
        return self._component_factory(component_data)
