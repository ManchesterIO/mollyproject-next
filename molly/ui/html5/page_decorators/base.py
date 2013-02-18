import hashlib
from flask import render_template

from flask.ext.assets import Bundle

class BasePageDecorator(object):

    css = frozenset()

    def __init__(self, assets):
        self._assets = assets

    def _build_bundle(self, css):
        hash = hashlib.md5()
        css = list(css) + list(self.css)
        for css_file in css:
            hash.update(css_file)
        hash = hash.hexdigest()
        if hash not in self._assets:
            self._assets.register(
                hash,
                Bundle(
                    *css,
                    filters=['cssmin', 'cssrewrite'],
                    output='stylec/{}.%(version)s.css'.format(hash)
                )
            )
        return hash

    def _render_template(self, template, component):
        return render_template(
            template,
            body=component,
            bundle=self._build_bundle(component.css)
        )
