from collections import namedtuple

class Identifier(namedtuple("Identifier", ["namespace", "value", "lang"])):

    def __new__(cls, namespace=None, value=None, lang=None):
        return super(Identifier, cls).__new__(cls, namespace, value, lang)

    def as_dict(self):
        serialised = {
            'namespace': self.namespace,
            'value': self.value
        }
        if self.lang is not None:
            serialised['lang'] = self.lang
        return serialised

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.as_dict().items()))


class Identifiers(set):

    def by_namespace(self, namespace):
        """
        Returns the subset of all identifiers in this list which have the given
        namespace.
        """
        results = set()
        for identifier in self:
            if identifier.namespace == namespace:
                results.add(identifier)
        return results