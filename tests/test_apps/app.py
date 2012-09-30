class App(object):

    def __init__(self, app, instance_name, config, providers=[]):
        self.app = app
        self.instance_name = instance_name
        self.config = config
        self.providers = providers
