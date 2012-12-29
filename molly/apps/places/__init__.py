from flask import Blueprint
from flask.ext.script import Command

class App(object):

    module = 'http://mollyproject.org/apps/places'

    def __init__(self, instance_name, config, providers, services):
        self.instance_name = instance_name

        for provider in providers:
            services['tasks'].periodic_task(provider.load, crontab=provider.IMPORT_SCHEDULE)
            command = Command()
            command.run = provider.load
            services['cli'].add_command(
                'import_{provider}_{instance_name}'.format(
                    provider=provider.IMPORTER_NAME, instance_name=instance_name
                ), command
            )

        self.blueprint = Blueprint(self.instance_name, __name__)