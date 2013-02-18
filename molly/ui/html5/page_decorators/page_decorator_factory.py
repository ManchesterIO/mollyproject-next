from molly.ui.html5.page_decorators.default import DefaultPageDecorator

class PageDecoratorFactory(object):

    def __init__(self, assets):
        self._default_decorator = DefaultPageDecorator(assets)

    def get_decorator(self, url):
        return self._default_decorator
