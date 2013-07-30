from molly.ui.html5.filters import register_filter

@register_filter('render')
def render(component, component_factory, **kwargs):
    return component_factory(component).render(**kwargs)