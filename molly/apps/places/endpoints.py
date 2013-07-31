from flask import url_for, redirect
from shapely.geometry import Point
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


class NearbySearchEndpoint(Endpoint):
    def __init__(self, instance_name, poi_service):
        self._poi_service = poi_service
        self._href = lambda lat, lon: url_for(instance_name + '.nearby', lat=lat, lon=lon, _external=True)
        self._poi_href = lambda slug: url_for(instance_name + '.poi', slug=slug, _external=True)

    def get(self, lat, lon):
        fixed_lat, fixed_lon = map(lambda l: round(l, 5), [lat, lon])
        if (fixed_lat, fixed_lon) != (lat, lon):
            return redirect(self._href(fixed_lat, fixed_lon))
        else:
            return self._json_response({
                'self': 'http://mollyproject.org/apps/places/points-of-interest',
                'points_of_interest': self._fetch_points_of_interest(fixed_lat, fixed_lon)
            })

    def _fetch_points_of_interest(self, lat, lon):
        pois = self._poi_service.search_nearby(Point(lon, lat))
        pois = map(lambda poi: poi._asdict(), pois)
        for poi in pois:
            poi['href'] = self._poi_href(poi['slug'])
        return pois
