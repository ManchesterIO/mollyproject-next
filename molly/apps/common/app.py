from flask.ext.script import Command

class BaseApp(object):

    def _register_provider_as_importer(self, provider, services):
        services['tasks'].periodic_task(provider.load, crontab=provider.IMPORT_SCHEDULE)
        command = Command()
        command.run = provider.load
        services['cli'].add_command(
            'import_{provider}_{instance_name}'.format(
                provider=provider.IMPORTER_NAME, instance_name=self.instance_name
            ), command
        )