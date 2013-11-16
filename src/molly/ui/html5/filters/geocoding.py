# coding=utf-8
import logging
import requests
from requests.exceptions import RequestException
from flask import current_app

LOGGER = logging.getLogger(__name__)
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours
CACHE_KEY = 'geolocation/reverse/{lat},{lon}'


def reverse_geocode(point):

    def _do_reverse_geocode(point):
        _URL = 'http://beta.geocoding.cloudmade.com/v3/{key}/api/geo.location.search.2?format=json&source=OSM&q=[latitude={lat}];[longitude={lon}]'
        fallback = u'{lat}˚, {lon}˚'.format(lat=point.y, lon=point.x)

        url = _URL.format(key=current_app.config['CLOUDMADE_API_KEY'], lat=point.y, lon=point.x)

        try:
            with current_app.statsd.timer(__name__ + '.reverse_geocode_time'):
                response = requests.get(url).json()
        except ValueError:
            LOGGER.exception('Failed to decode response from Cloudmade: %s', url)
            current_app.statsd.incr(__name__ + '.reverse_geocode_json_parse_error')
            return fallback, False
        except RequestException:
            LOGGER.exception('Request to Cloudmade failed: %s', url)
            current_app.statsd.incr(__name__ + '.reverse_geocode_request_exception')
            return fallback, False

        if not response.get('status', {}).get('success'):
            LOGGER.info("Reverse Geocode returns no results for: %d, %d", point.y, point.x)
            current_app.statsd.incr(__name__ + '.reverse_geocode_failed')
            return fallback, False
        else:
            current_app.statsd.incr(__name__ + '.reverse_geocode_success')
            result = response['places'][0]
            for key in ['name', 'street', 'district', 'city']:
                if key in result:
                    return result[key].strip('~'), True

        return fallback, False

    cache_key = CACHE_KEY.format(lat=point.y, lon=point.x)
    cached_result = current_app.cache.get(cache_key)
    if cached_result:
        current_app.statsd.incr(__name__ + '.reverse_geocode_cache_hit')
        return cached_result
    else:
        current_app.statsd.incr(__name__ + '.reverse_geocode_cache_miss')
        result, success = _do_reverse_geocode(point)
        if success:
            current_app.cache.set(cache_key, result, CACHE_TIMEOUT)
        return result