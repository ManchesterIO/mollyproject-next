from molly.ui.html5.components.component import Component


class ComponentFactory(object):

    _components = {}

    @classmethod
    def register_component(cls, url):
        def _register_component(klass):
            cls._components[url] = klass
            return klass
        return _register_component

    def __call__(self, obj):
        return self._components.get(obj['self'], Component)(obj, self)
