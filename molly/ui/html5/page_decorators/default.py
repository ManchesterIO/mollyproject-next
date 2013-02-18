from molly.ui.html5.page_decorators.base import BasePageDecorator

class DefaultPageDecorator(BasePageDecorator):

    css = frozenset({'style/vendors/normalize.css', 'style/base.css'})

    def __call__(self, component):
        return self._render_template('default.html', component)
