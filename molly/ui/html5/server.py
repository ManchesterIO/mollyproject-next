from shutil import copyfile
import os

from flask import Flask
from flask.ext.assets import Environment as Assets
from flask.ext.babel import Babel
from flask.ext.cache import Cache
from flask.ext.statsd import StatsD
from jinja2 import PackageLoader, ChoiceLoader, PrefixLoader, FileSystemLoader, MemcachedBytecodeCache
from raven.contrib.flask import Sentry

from molly.services.stats import NullStats
from molly.ui.html5.components.factory import ComponentFactory
from molly.ui.html5.filters import FILTERS as filters
from molly.ui.html5.page_decorators.page_decorator_factory import PageDecoratorFactory
from molly.ui.html5.request_factory import HttpRequestFactory
from molly.ui.html5.router import Router, StaticPageRouter


def init_flask():
    flask_app = Flask(__name__)
    flask_app.config.from_envvar('MOLLY_UI_SETTINGS')
    Babel(flask_app)
    if 'SENTRY_DSN' in flask_app.config:
        Sentry(flask_app)
    statsd = StatsD(flask_app) if 'STATSD_HOST' in flask_app.config else NullStats()
    return flask_app, statsd
flask_app, statsd = init_flask()


def init_molly(flask_app, api_hostname, api_port):
    request_factory = HttpRequestFactory(hostname=api_hostname, port=api_port)
    component_factory = ComponentFactory()
    assets = Assets(flask_app)
    if flask_app.debug:
        assets.debug = True
    page_decorator_factory = PageDecoratorFactory(assets)

    router = Router(request_factory, component_factory, page_decorator_factory, statsd)

    flask_app.add_url_rule('/', 'homepage', view_func=router)
    flask_app.add_url_rule('/<path:path>', 'main', view_func=router)
    flask_app.add_url_rule('/about', 'about', view_func=StaticPageRouter('about.html'))
    flask_app.add_url_rule('/developers', 'developers', view_func=StaticPageRouter('developers.html'))
    flask_app.add_url_rule('/privacy', 'privacy', view_func=StaticPageRouter('privacy.html'))

    for filter_name, filter_func in filters.items():
        flask_app.jinja_env.filters[filter_name] = filter_func


def configure_template_loader(flask_app, template_dir, cache):
    if template_dir:
        loaders = [FileSystemLoader(template_dir)]
    else:
        loaders = []

    flask_app.jinja_loader = ChoiceLoader(loaders + [
        PackageLoader('molly.ui.html5', 'templates'),
        PrefixLoader({'molly_default': PackageLoader('molly.ui.html5', 'templates')})
    ])

    if cache:
        flask_app.jinja_env.bytecode_cache = MemcachedBytecodeCache(cache)


def collect_static(override_location, output_location, debug):
    asset_paths = [os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets')]
    if override_location:
        asset_paths.append(override_location)

    for root in asset_paths:
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                source = os.path.join(dirpath, filename)
                destination = os.path.join(output_location, dirpath[len(root)+1:], filename)
                print source, destination
                if not os.path.exists(os.path.dirname(destination)):
                    os.makedirs(os.path.dirname(destination))
                if debug:
                    if os.path.exists(destination):
                        os.remove(destination)
                    os.symlink(source, destination)
                else:
                    copyfile(source, destination)


def start_debug(address=None):
    flask_app.debug = True
    cache = Cache(flask_app)
    init_molly(
        flask_app,
        flask_app.config.get('MOLLY_API_HOSTNAME', 'localhost'),
        flask_app.config.get('MOLLY_API_PORT', 8000)
    )
    configure_template_loader(flask_app, flask_app.config.get('TEMPLATE_DIR'), cache)

    flask_app.static_folder = flask_app.config.get('ASSET_DIR')
    flask_app.static_url_path = 'static'

    collect_static(flask_app.config.get('OVERRIDE_ASSET_DIR'), flask_app.static_folder, True)

    flask_app.run(debug=True, host=address, port=8002)
