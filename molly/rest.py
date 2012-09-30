import os

from flask import Flask

from molly.config import ConfigLoader
from molly.apps.homepage import App as Homepage

flask_app = Flask(__name__)

with open(os.environ.get('MOLLY_CONFIG', 'conf/default.conf')) as fd:
    config_loader = ConfigLoader()
    apps = config_loader.load_from_config(fd)

for app in apps:
    flask_app.register_blueprint(app.blueprint, url_prefix='/' + app.instance_name)
flask_app.register_blueprint(Homepage(apps).blueprint)
