from molly.ui.html5.page_decorators.base import BasePageDecorator

class HomepageDecorator(BasePageDecorator):

    def handles_url(self, url):
        return url == '/'

    def __call__(self, component):
        return self._render_template('base.html', component)
