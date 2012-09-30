from flask import Blueprint

from molly.apps.homepage.endpoints import HomepageEndpoint

class App(object):

    def __init__(self, apps):
        self.blueprint = Blueprint('homepage', __name__)
        self.blueprint.add_url_rule('/', 'index', HomepageEndpoint(apps).get)
