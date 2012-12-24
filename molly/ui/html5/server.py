from flask import Flask
from flask.ext.babel import Babel
from jinja2 import PackageLoader

from molly.ui.html5.components.factory import ComponentFactory
from molly.ui.html5.page_decorators.page_decorator_factory import PageDecoratorFactory
from molly.ui.html5.request_factory import HttpRequestFactory
from molly.ui.html5.router import Router

flask_app = Flask(__name__)
Babel(flask_app)

request_factory = HttpRequestFactory(hostname='localhost', port=8000)
component_factory = ComponentFactory()
page_decorator_factory = PageDecoratorFactory()
router = Router(request_factory, component_factory, page_decorator_factory)

flask_app.add_url_rule('/', 'homepage', view_func=router)
flask_app.add_url_rule('/<path:path>', 'main', view_func=router)

flask_app.jinja_loader = PackageLoader('molly.ui.html5', 'templates')
