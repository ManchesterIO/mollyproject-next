from flask import url_for
from werkzeug.exceptions import abort

from molly.apps.common.endpoints import Endpoint


class PointOfInterestEndpoint(Endpoint):

    def __init__(self, instance_name, poi_service):
        self._poi_service = poi_service
        self._href = lambda slug: url_for(instance_name + '.poi', slug=slug, _external=True)

    def get(self, slug):
        poi = self._poi_service.select_by_slug(slug)
        if poi is None:
            abort(404)
        else:
            return self._json_response({
                'self': 'http://mollyproject.org/apps/places/point-of-interest',
                'href': self._href(slug),
                'poi': poi._asdict()
            })