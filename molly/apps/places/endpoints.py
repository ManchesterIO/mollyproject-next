from flask import url_for, redirect
from shapely.geometry import Point
from werkzeug.exceptions import abort

from molly.apps.common.endpoints import Endpoint


class PointOfInterestEndpoint(Endpoint):

    def __init__(self, instance_name, poi_service):
        self._poi_service = poi_service
        self._href = lambda slug: url_for(instance_name + '.poi', slug=slug, _external=True)
        self._nearby_href = lambda lat, lon: url_for(instance_name + '.nearby', lat=lat, lon=lon, _external=True)

    def get(self, slug):
        poi = self._poi_service.select_by_slug(slug)
        if poi is None:
            abort(404)
        else:
            links = {

            }
            if poi.location:
                links['nearby'] = self._nearby_href(poi.location.y, poi.location.x)
            return self._json_response({
                'self': 'http://mollyproject.org/apps/places/point-of-interest',
                'href': self._href(slug),
                'poi': poi._asdict(),
                'links': links
            })


DEFAULT_INTERESTING_CATEGORIES = {
    'air-line': 'http://mollyproject.org/poi/types/transport/air-line',
    'airport': 'http://mollyproject.org/poi/types/transport/airport',
    'arts-centre': 'http://mollyproject.org/poi/types/leisure/arts-centre',
    'bank': 'http://mollyproject.org/poi/types/retail/bank',
    'bar': 'http://mollyproject.org/poi/types/leisure/bar',
    'bench': 'http://mollyproject.org/poi/types/leisure/bench',
    'bicycle-parking': 'http://mollyproject.org/poi/transport/parking/bicycle',
    'bicycle-rental': 'http://mollyproject.org/poi/types/transport/bicycle-rental',
    'bus-stop': 'http://mollyproject.org/poi/types/transport/bus-stop',
    'cinema': 'http://mollyproject.org/poi/types/leisure/cinema',
    'dlr-station': 'http://mollyproject.org/poi/types/transport/dlr-station',
    'health': 'http://mollyproject.org/poi/types/health',
    'ice-rink': 'http://mollyproject.org/poi/types/leisure/ice-rink',
    'food': 'http://mollyproject.org/poi/types/food',
    'ferry-terminal': 'http://mollyproject.org/poi/types/transport/ferry-terminal',
    'fuel': 'http://mollyproject.org/poi/types/transport/fuel',
    'gatwick-shuttle-station': 'http://mollyproject.org/poi/types/transport/gatwick-shuttle-station',
    'heritage-rail-station': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
    'library': 'http://mollyproject.org/poi/types/leisure/library',
    'marketplace': 'http://mollyproject.org/poi/types/retail/marketplace',
    'metrolink-station': 'http://mollyproject.org/poi/types/transport/metrolink-station',
    'midland-metro-stop': 'http://mollyproject.org/poi/types/transport/midland-metro-stop',
    'museum': 'http://mollyproject.org/poi/types/leisure/museum',
    'net-stop': 'http://mollyproject.org/poi/types/transport/net-stop',
    'nightclub': 'http://mollyproject.org/poi/types/leisure/nightclub',
    'park': 'http://mollyproject.org/poi/types/leisure/park',
    'parking': 'http://mollyproject.org/poi/types/transport/parking/car',
    'place-of-worship': 'http://mollyproject.org/poi/types/place-of-worship',
    'police': 'http://mollyproject.org/poi/types/police-station',
    'post-office': 'http://mollyproject.org/poi/types/retail/post-office',
    'pub': 'http://mollyproject.org/poi/types/leisure/pub',
    'punt-hire': 'http://mollyproject.org/poi/types/leisure/punt-hire',
    'subway-station': 'http://mollyproject.org/poi/types/transport/subway-station',
    'taxi-rank': 'http://mollyproject.org/poi/types/transport/taxi-rank',
    'theatre': 'http://mollyproject.org/poi/types/leisure/theatre',
    'tramway-stop': 'http://mollyproject.org/poi/types/transport/tramway-stop',
    'tramlink-stop':'http://mollyproject.org/poi/types/transport/tramlink-stop',
    'tube-station': 'http://mollyproject.org/poi/types/transport/tube-station',
    'rail-station': 'http://mollyproject.org/poi/types/transport/rail-station',
    'sports-centre': 'http://mollyproject.org/poi/types/leisure/sports-centre',
    'supertram-stop': 'http://mollyproject.org/poi/types/transport/supertram-stop',
    'swimming-pool': 'http://mollyproject.org/poi/types/leisure/swimming-pool',
    'tourist-information': 'http://mollyproject.org/poi/types/tourist-information',
    'tyne-and-wear-metro-station': 'http://mollyproject.org/poi/types/transport/tyne-and-wear-metro-station',
}


DEFAULT_INTERESTING_AMENITIES = {
    'atm': 'http://mollyproject.org/poi/amenities/atm',
    'post-box': 'http://mollyproject.org/poi/amenities/post-box',
    'recycling': 'http://mollyproject.org/poi/amenities/recycling',
    'telephone': 'http://mollyproject.org/poi/amenities/telephone',
    'tourist-attraction': 'http://mollyproject.org/poi/amenities/tourist-attraction',
}


class NearbySearchEndpoint(Endpoint):

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
        self.interesting_categories = dict(DEFAULT_INTERESTING_CATEGORIES.items())
        self.interesting_amenities = dict(DEFAULT_INTERESTING_AMENITIES.items())


    def _get_nearby_categories(self, point):
        categories = []
        for slug, category in self.interesting_categories.items():
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
        for slug, amenity in self.interesting_amenities.items():
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
            category = self._get_uri_from_slug(slug, self.interesting_categories)
            points_of_interest = self._poi_service.search_nearby_category(
                Point(lon, lat), category, radius=self.SEARCH_RADIUS
            )
            return self._build_poi_list(points_of_interest, 'category', category)

    def get_amenity(self, lat, lon, slug):
        lat, lon, needs_redirect = self._needs_redirect(lat, lon)
        if needs_redirect:
            return redirect(self._nearby_amenity_href(lat, lon, slug))
        else:
            amenity = self._get_uri_from_slug(slug, self.interesting_amenities)
            points_of_interest = self._poi_service.search_nearby_amenity(
                Point(lon, lat), amenity, radius=self.SEARCH_RADIUS
            )
            return self._build_poi_list(points_of_interest, 'amenity', amenity)

    def _build_poi_list(self, points_of_interest, filter_key, filter_value):
        return self._json_response({
            'self': 'http://mollyproject.org/apps/places/points-of-interest/by-' + filter_key,
            filter_key: filter_value,
            'points_of_interest': map(lambda poi: {
                'self': 'http://mollyproject.org/apps/places/point-of-interest',
                'href': self._poi_href(poi.slug),
                'poi': poi._asdict()
            }, points_of_interest),
            'count': len(points_of_interest),
            'within': self.SEARCH_RADIUS
        })

    def _get_uri_from_slug(self, slug, interesting_things):
        uri = interesting_things.get(slug)
        if uri is None:
            abort(404)
        else:
            return uri
