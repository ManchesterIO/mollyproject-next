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

    INTERESTING_CATEGORIES = {}
    INTERESTING_AMENITIES = {}
    SEARCH_RADIUS = 1610  # 1610 metres ~ 1 mile

    def __init__(self, instance_name, poi_service):
        self._poi_service = poi_service
        self._href = lambda lat, lon: url_for(instance_name + '.nearby', lat=lat, lon=lon, _external=True)
        self._poi_href = lambda slug: url_for(instance_name + '.poi', slug=slug, _external=True)
        self._nearby_amenity_href = lambda lat, lon, slug: url_for(
            instance_name + '.nearby_amenity', lat=lat, lon=lon, slug=slug, _external=True
        )
        self._nearby_category_href = lambda lat, lon, slug: url_for(
            instance_name + '.nearby_category', lat=lat, lon=lon, slug=slug, _external=True
        )

    def _get_nearby_categories(self, point):
        categories = []
        for slug, category in self.INTERESTING_CATEGORIES.items():
            num_pois = self._poi_service.count_nearby_category(point, category, radius=self.SEARCH_RADIUS)
            if num_pois > 0:
                categories.append({
                    'self': 'http://mollyproject.org/apps/places/points-of-interest/by-category',
                    'href': self._nearby_category_href(point.y, point.x, slug),
                    'category': category,
                    'count': num_pois,
                    'within': self.SEARCH_RADIUS
                })
        return categories

    def _get_nearby_amenities(self, point):
        amenities = []
        for slug, amenity in self.INTERESTING_AMENITIES.items():
            num_pois = self._poi_service.count_nearby_amenity(point, amenity, radius=self.SEARCH_RADIUS)
            if num_pois > 0:
                amenities.append({
                    'self': 'http://mollyproject.org/apps/places/points-of-interest/by-amenity',
                    'href': self._nearby_amenity_href(point.y, point.x, slug),
                    'amenity': amenity,
                    'count': num_pois,
                    'within': self.SEARCH_RADIUS
                })
        return amenities

    def _needs_redirect(self, lat, lon):
        fixed_lat, fixed_lon = map(lambda l: round(l, 5), (lat, lon))
        needs_redirect = (fixed_lat, fixed_lon) != (lat, lon)
        return fixed_lat, fixed_lon, needs_redirect

    def get_categories(self, lat, lon):
        lat, lon, needs_redirect = self._needs_redirect(lat, lon)
        if needs_redirect:
            return redirect(self._href(lat, lon))
        else:
            point = Point(lon, lat)
            return self._json_response({
                'self': 'http://mollyproject.org/apps/places/categories',
                'categories': self._get_nearby_categories(point),
                'amenities': self._get_nearby_amenities(point)
            })

    def get_category(self, lat, lon, slug):
        lat, lon, needs_redirect = self._needs_redirect(lat, lon)
        if needs_redirect:
            return redirect(self._nearby_category_href(lat, lon, slug))
        else:
            category = self.INTERESTING_CATEGORIES.get(slug)
            if category is None:
                abort(404)
            else:
                points_of_interest = self._poi_service.search_nearby_category(
                    Point(lon, lat), category, radius=self.SEARCH_RADIUS
                )
                return self._json_response({
                    'self': 'http://mollyproject.org/apps/places/points-of-interest/by-category',
                    'category': category,
                    'points_of_interest': map(lambda poi: poi._asdict(), points_of_interest),
                    'count': len(points_of_interest),
                    'within': self.SEARCH_RADIUS
                })

    def get_amenity(self, lat, lon, slug):
        lat, lon, needs_redirect = self._needs_redirect(lat, lon)
        if needs_redirect:
            return redirect(self._nearby_amenity_href(lat, lon, slug))
        else:
            amenity = self.INTERESTING_AMENITIES.get(slug)
            if amenity is None:
                abort(404)
            else:
                points_of_interest = self._poi_service.search_nearby_amenity(
                    Point(lon, lat), amenity, radius=self.SEARCH_RADIUS
                )
                return self._json_response({
                    'self': 'http://mollyproject.org/apps/places/points-of-interest/by-amenity',
                    'amenity': amenity,
                    'points_of_interest': map(lambda poi: poi._asdict(), points_of_interest),
                    'count': len(points_of_interest),
                    'within': self.SEARCH_RADIUS
                })
