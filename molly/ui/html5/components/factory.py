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
        if isinstance(obj, Component):
            return obj
        else:
            if hasattr(obj, '_asdict'):
                obj = obj._asdict()
            component = self._components.get(obj['self'], Component)
            return component(obj, self)
