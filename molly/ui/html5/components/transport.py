from flask import render_template
from molly.ui.html5.components import ComponentFactory, Component

@ComponentFactory.register_component('http://mollyproject.org/apps/transport')
class TransportHomepage(Component):

    def __init__(self, *args, **kwargs):
        super(TransportHomepage, self).__init__(*args, **kwargs)
        self._components = map(self._load_component, self._data.get('links', []))

    def render(self):
        return ''
