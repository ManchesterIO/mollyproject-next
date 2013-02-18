from molly.ui.html5.components.component import Component
from molly.ui.html5.components.factory import ComponentFactory

@ComponentFactory.register_component('http://mollyproject.org/common/attribution')
class Attribution(Component):

    def render(self):
        return 'Attribution'
