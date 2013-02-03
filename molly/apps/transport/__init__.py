from flask import Blueprint
from flask.ext.babel import lazy_gettext as _
from molly.apps.common.app import BaseApp
from molly.apps.transport.services import LocalityService, StopService

class App(BaseApp):

    module = 'http://mollyproject.org/apps/transport'
    human_name = _('Transport')

    def __init__(self, instance_name, config, providers, services):
        self.instance_name = instance_name
        self.blueprint = Blueprint(self.instance_name, __name__)
        self.links = []

        locality_service = LocalityService(services['kv'].db[instance_name])
        stop_service = StopService(services['kv'].db[instance_name])

        for provider in providers:
            provider.locality_service = locality_service
            provider.stop_service = stop_service
            self._register_provider_as_importer(provider, services)