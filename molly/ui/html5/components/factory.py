from molly.ui.html5.components.component import Component

class ComponentFactory(object):

    def __call__(self, obj):
        return Component(obj)
