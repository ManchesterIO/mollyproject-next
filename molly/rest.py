import os

from flask import Flask

from molly.config import ConfigLoader
from molly.apps.homepage import App as Homepage

flask_app = Flask(__name__)

with open(os.environ.get('MOLLY_CONFIG', 'conf/default.conf')) as fd:
    config_loader = ConfigLoader()
    config, apps, services = config_loader.load_from_config(fd)

flask_app.config.update(config)

for service in services.values():
    service.init_app(flask_app)

for app in apps:
    flask_app.register_blueprint(app.blueprint, url_prefix='/' + app.instance_name)
flask_app.register_blueprint(Homepage(apps).blueprint)

def start_debug(address=None):
    flask_app.debug = True
    flask_app.run(debug=True, host=address, port=8000)
