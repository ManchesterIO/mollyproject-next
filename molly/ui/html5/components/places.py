from molly.ui.html5.components import ComponentFactory, Component

@ComponentFactory.register_component('http://mollyproject.org/apps/places')
class PlacesHomepage(Component):

    def __init__(self, *args, **kwargs):
        super(PlacesHomepage, self).__init__(*args, **kwargs)
        self._components = map(self._load_component, self._data.get('links', []))

    def render(self):
        return ''
