from molly.apps.common.endpoints import Endpoint

class HomepageEndpoint(Endpoint):

    def __init__(self, apps):
        self._apps = apps

    def get(self):
        return self._json_response({
            'applications': self._get_apps_json()
        })

    def _get_apps_json(self):
        apps_json = []
        for app in self._apps:
            apps_json.append(self._get_app_json(app))
        return apps_json

    def _get_app_json(self, app):
        return {
            'module': app.module,
            'instance_name': app.instance_name,
            'human_name': app.human_name,
            'index_url': app.index_url,
            'widget_params': app.homepage_widget_params
        }
