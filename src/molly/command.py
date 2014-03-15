from gunicorn.app.base import Application


def configure_manager(manager, flask_app, debug, default_port=8000):

    def start(port=default_port):
        class MollyApplication(Application):

            def init(self, parser, opts, args):
                self.cfg.set('bind', '127.0.0.1:{}'.format(port))

            def load(self):
                return flask_app

        MollyApplication().run()
    manager.command(start)

    if debug is not None:
        manager.command(debug)

    return manager


def main():
    from molly.rest import flask_app, cli_manager, start_debug
    configure_manager(cli_manager, flask_app, start_debug).run()
