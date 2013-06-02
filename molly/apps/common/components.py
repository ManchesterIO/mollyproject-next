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

    @classmethod
    def from_dict(cls, attribution):
        if attribution is None:
            return None
        else:
            return cls(
                licence_name=attribution.get('licence_name'),
                licence_url=attribution.get('licence_url'),
                attribution_text=attribution.get('attribution_text'),
                attribution_url=attribution.get('attribution_url')
            )


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


class LocalisedNames(set):

    def language(self, lang=None):
        for name, lang_code in self:
            if lang == lang_code:
                return name
        else:
            return None

    def language_codes(self):
        return [name.lang for name in self if name.lang is not None]


class Source(namedtuple('Source', ['url', 'version', 'attribution'])):
    def _asdict(self):
        return {
            'self': 'http://mollyproject.org/common/source',
            'url': self.url,
            'version': self.version,
            'attribution': self.attribution._asdict() if self.attribution is not None else None
        }

    @classmethod
    def from_dict(cls, source):
        return cls(source['url'], source['version'], Attribution.from_dict(source['attribution']))