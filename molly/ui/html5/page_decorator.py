class PageDecorator(object):

    def __call__(self, component):
        return '<pre>{}</pre>'.format(component.render())
