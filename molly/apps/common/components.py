from collections import namedtuple

class Attribution(object):

    def __init__(self, licence_name=None, licence_url=None, attribution_text=None, attribution_url=None):
        self.licence_name = licence_name
        self.licence_url = licence_url
        self.attribution_text = attribution_text
        self.attribution_url = attribution_url

    def _asdict(self):
        return {
            'self': 'http://mollyproject.org/common/attribution',
            'licence_name': self.licence_name,
            'licence_url': self.licence_url,
            'attribution_text': self.attribution_text,
            'attribution_url': self.attribution_url
        }


Identifier = namedtuple('Identifier', ['namespace', 'value'])


class Identifiers(set):

    def by_namespace(self, namespace):
        """
        the subset of all identifiers in this set which have the given namespace.
        """
        results = set()
        for identifier in self:
            if identifier.namespace == namespace:
                results.add(identifier)
        return results


LocalisedName = namedtuple('LocalisedName', ['name', 'lang'])
Source = namedtuple('Source', ['url', 'version', 'attribution'])