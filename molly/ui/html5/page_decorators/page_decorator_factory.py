from molly.ui.html5.page_decorators.default import DefaultPageDecorator
from molly.ui.html5.page_decorators.homepage import HomepagePageDecorator

class PageDecoratorFactory(object):

    def __init__(self):
        self._homepage_decorator = HomepagePageDecorator()
        self._default_decorator = DefaultPageDecorator()

    def get_decorator(self, url):
        if url == '':
            return self._homepage_decorator
        else:
            return self._default_decorator
