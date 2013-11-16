from molly.apps.common.endpoints import Endpoint

class HomepageEndpoint(Endpoint):

    def __init__(self, apps):
        self._apps = apps

    def get(self):
        return self._json_response({
            'self': 'http://mollyproject.org/apps/homepage',
            'applications': self._get_apps_json()
        })

    def _get_apps_json(self):
        apps_json = []
        for app in self._apps:
            apps_json.append(self._get_app_json(app))
        return apps_json

    def _get_app_json(self, app):
        return {
            'self': app.module,
            'instance_name': app.instance_name,
            'human_name': app.human_name,
            'links': app.links
        }
