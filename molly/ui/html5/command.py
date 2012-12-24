import os.path

from flask.ext.script import Manager
from gunicorn.app.base import Application

from molly.ui.html5.server import flask_app

manager = Manager(flask_app, with_default_commands=False)

@manager.command
def start():
    class MollyApplication(Application):

        def init(self, parser, opts, args):
            pass

        def load(self):
            return flask_app

    MollyApplication().run()

@manager.command
def debug():
    flask_app.debug = True
    flask_app.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
    flask_app.static_url_path = 'static'
    flask_app.run(debug=True, port=8002)

def main():
    manager.run()

if __name__ == '__main__':
    main()