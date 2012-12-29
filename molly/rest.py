import os

from flask import Flask
from flask.ext.script import Manager

from molly.config import ConfigLoader
from molly.apps.homepage import App as Homepage

def configure_flask_app():
    flask_app = Flask(__name__)

    with open(os.environ.get('MOLLY_CONFIG', 'conf/default.conf')) as fd:
        config_loader = ConfigLoader(flask_app)
        config, apps, services = config_loader.load_from_config(fd)

    flask_app.config.update(config)

    for service in services.values():
        if hasattr(service, 'init_app'):
            service.init_app(flask_app)
        if hasattr(service, 'init_cli_commands'):
            service.init_cli_commands(services['cli'])

    for app in apps:
        flask_app.register_blueprint(app.blueprint, url_prefix='/' + app.instance_name)
    flask_app.register_blueprint(Homepage(apps).blueprint)

    return flask_app, services['cli']

def start_debug(address=None):
    flask_app.debug = True
    flask_app.run(debug=True, host=address, port=8000)

flask_app, cli_manager = configure_flask_app()