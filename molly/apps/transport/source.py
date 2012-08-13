class Source(object):

    def __init__(self, url=None, version=None, attribution=None, licence=None, licence_url=None):
        """
        :param url: a URI identifying the artifact which yielded that item this source is attached to
        :param version: some source artifacts are versioned, this captures that - any versioning scheme can be used
        :param attribution: a free-form text string
        :param licence: the name of the licence which applies to data from this source
        """
        self.url = url
        self.version = version
        self.attribution = attribution
        self.licence = licence
        self.licence_url = licence_url

    def as_dict(self):
        return {
            'url': self.url,
            'version': self.version,
            'attribution': self.attribution,
            'licence': self.licence,
            'licence_url': self.licence_url
        }

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()
