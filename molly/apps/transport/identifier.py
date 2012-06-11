class Identifier(object):

    def __init__(self, namespace=None, value=None):
        self.namespace = namespace
        self.value = value

    def as_dict(self):
        return {
            'namespace': self.namespace,
            'value': self.value
        }

class IdentifierList(list):

    def by_namespace(self, namespace):
        for identifier in self:
            if identifier.namespace == namespace:
                return identifier.value