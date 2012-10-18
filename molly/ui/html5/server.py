from flask import Flask
from molly.ui.html5.components.factory import ComponentFactory
from molly.ui.html5.page_decorator import PageDecorator

from .router import Router
from .request_factory import HttpRequestFactory

flask_app = Flask(__name__)
flask_app.debug = True

request_factory = HttpRequestFactory(hostname='localhost', port=8000)
component_factory = ComponentFactory()
page_decorator = PageDecorator()
router = Router(request_factory, component_factory, page_decorator)

flask_app.add_url_rule('/', 'homepage', view_func=router)
flask_app.add_url_rule('/<path:path>', 'main', view_func=router)
