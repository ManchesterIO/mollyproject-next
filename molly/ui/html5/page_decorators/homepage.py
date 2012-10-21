from flask import render_template

from molly.ui.html5.page_decorators.base import BasePageDecorator

class HomepagePageDecorator(BasePageDecorator):

    def __call__(self, component):
        return self._render_template('default.html', component)
