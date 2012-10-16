class Attribution(object):

    def __init__(self, licence_name=None, licence_url=None, attribution_text=None):
        self.licence_name = licence_name
        self.licence_url = licence_url
        self.attribution_text = attribution_text

    def as_dict(self):
        return {
            'self': 'http://mollyproject.org/common/attribution',
            'licence_name': self.licence_name,
            'licence_url': self.licence_url,
            'attribution_text': self.attribution_text
        }
