from molly.ui.html5.page_decorators.default import DefaultPageDecorator
from molly.ui.html5.page_decorators.homepage import HomepageDecorator

class PageDecoratorFactory(object):

    def __init__(self, assets):
        self._default_decorator = DefaultPageDecorator(assets)
        self._decorators = map(lambda decorator: decorator(assets), [
            HomepageDecorator
        ])

    def get_decorator(self, url):
        for decorator in self._decorators:
            if decorator.handles_url(url):
                return decorator
        return self._default_decorator
