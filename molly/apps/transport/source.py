class Source(object):

    def __init__(self, url=None, version=None):
        self.url = url
        self.version = version

    def as_dict(self):
        return {
            'url': self.url,
            'version': self.version
        }