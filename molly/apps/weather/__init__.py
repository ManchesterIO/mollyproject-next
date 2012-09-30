from flask import Blueprint, url_for
from flaskext.babel import lazy_gettext as _

from molly.apps.weather.endpoints import ObservationsEndpoint

class App(object):

    module = __name__

    def __init__(self, instance_name, config, providers=[]):
        self.instance_name = instance_name
        self.blueprint = Blueprint('weather', __name__)
        self.blueprint.add_url_rule('/', 'observations', ObservationsEndpoint(providers.pop()).get)

        self.homepage_widget_params = {}
        self.human_name = _('Weather')

    @property
    def index_url(self):
        return url_for('weather.observations')
