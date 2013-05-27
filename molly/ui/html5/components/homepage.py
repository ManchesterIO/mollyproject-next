from flask import render_template
from jinja2 import Markup
from molly.ui.html5.components.component import Component
from molly.ui.html5.components.factory import ComponentFactory


@ComponentFactory.register_component('http://mollyproject.org/apps/homepage')
class Homepage(Component):

    _CSS = frozenset(['style/components/homepage.css'])

    def __init__(self, *args, **kwargs):
        super(Homepage, self).__init__(*args, **kwargs)
        self._applications = []
        for application in self._data['applications']:
            self._applications.append(self._load_component(application))

    @property
    def title(self):
        return 'Home'

    def render(self):
        return Markup(render_template('apps/homepage.html', applications=self._applications))
