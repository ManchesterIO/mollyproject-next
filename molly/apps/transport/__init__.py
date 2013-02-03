from flask import Blueprint
from flask.ext.babel import lazy_gettext as _

class App(object):

    module = 'http://mollyproject.org/apps/transport'
    human_name = _('Transport')

    def __init__(self, instance_name, config, providers, services):
        self.instance_name = instance_name
        self.blueprint = Blueprint(self.instance_name, __name__)
        self.links = []