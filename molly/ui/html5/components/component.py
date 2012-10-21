from urlparse import urlparse

class Component(object):

    _CSS = frozenset()
    _JS = frozenset()

    def __init__(self, data, component_factory):
        self._data = data
        self._component_factory = component_factory
        self._css = set(self._CSS)
        self._js = set(self._JS)

    @property
    def title(self):
        raise NotImplementedError()

    @property
    def href(self):
        return urlparse(self._data.get('href')).path

    @property
    def css(self):
        print self._css
        return list(self._css)

    @property
    def js(self):
        print self._js
        return list(self._js)

    def render(self):
        raise NotImplementedError()

    def _add_css(self, css):
        self._css.add(css)

    def _add_js(self, js):
        self._js.add(js)

    def _load_component(self, component_data):
        component = self._component_factory(component_data)
        print component
        for css in component.css: self._add_css(css)
        for js in component.js :self._add_js(js)
        return component
