from flask import Blueprint
from flask.ext.babel import lazy_gettext as _
from flask.ext.script import Command

from molly.apps.places.services import PointsOfInterest

class App(object):

    module = 'http://mollyproject.org/apps/places'
    human_name = _('Places')

    def __init__(self, instance_name, config, providers, services):
        self.instance_name = instance_name
        poi_service = PointsOfInterest(instance_name, services['kv'], services['search'])

        for provider in providers:
            provider.poi_service = poi_service
            services['tasks'].periodic_task(provider.load, crontab=provider.IMPORT_SCHEDULE)
            command = Command()
            command.run = provider.load
            services['cli'].add_command(
                'import_{provider}_{instance_name}'.format(
                    provider=provider.IMPORTER_NAME, instance_name=instance_name
                ), command
            )

        self.blueprint = Blueprint(self.instance_name, __name__)
        self.links = []