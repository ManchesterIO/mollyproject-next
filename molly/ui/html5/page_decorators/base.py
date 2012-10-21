from flask import render_template

class BasePageDecorator(object):

    def _render_template(self, template, component):
        print component.css
        return render_template(
            template,
            body=component,
            css=['vendors/normalize.css', 'base.css'] + component.css
        )
