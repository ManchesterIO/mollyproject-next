from flask import Blueprint
from flask.ext.babel import lazy_gettext as _

from molly.apps.common.app import BaseApp
from molly.apps.places.endpoints import PointOfInterestEndpoint, NearbySearchEndpoint
from molly.apps.places.services import PointsOfInterest


class App(BaseApp):

    module = 'http://mollyproject.org/apps/places'
    human_name = _('Places')

    def __init__(self, instance_name, config, providers, services):
        self.instance_name = instance_name
        poi_service = PointsOfInterest(instance_name, services['kv'].db[instance_name])

        for provider in providers:
            provider.poi_service = poi_service
            self._register_provider_as_importer(provider, services)

        self._poi_endpoint = PointOfInterestEndpoint(instance_name, poi_service)
        self._nearby_search_endpoint = NearbySearchEndpoint(instance_name, poi_service)

        self.blueprint = Blueprint(self.instance_name, __name__)
        self.blueprint.add_url_rule('/<slug>/', 'poi', self._poi_endpoint.get)
        self.blueprint.add_url_rule('/nearby/<float:lat>,<float:lon>/', 'nearby', self._nearby_search_endpoint.get_categories)
        self.links = []
