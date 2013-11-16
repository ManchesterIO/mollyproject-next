from flask import render_template
from flask.ext.assets import Bundle


class BasePageDecorator(object):

    css = frozenset()

    def __init__(self, assets):
        self._assets = assets

    def _build_bundle(self):
        bundle_name = 'molly'
        if bundle_name not in self._assets:
            self._assets.register(
                bundle_name,
                Bundle(
                    'sass/app.scss',
                    filters=['compass', 'cssmin', 'cssrewrite'],
                    output='stylec/%(version)s.css'
                )
            )
        return bundle_name

    def _render_template(self, template, component, **kwargs):
        return render_template(
            template,
            body=component,
            bundle=self._build_bundle(),
            **kwargs
        )

    def handles_url(self, url):
        return False
