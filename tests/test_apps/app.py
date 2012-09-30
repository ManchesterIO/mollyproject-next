class App(object):

    def __init__(self, instance_name, config, providers=[]):
        self.instance_name = instance_name
        self.config = config
        self.providers = providers
