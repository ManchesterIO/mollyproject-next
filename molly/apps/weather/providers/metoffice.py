# coding=utf-8
from datetime import timedelta, datetime
import json
from string import capwords
from pytz import utc
import time
from urllib2 import urlopen

from flaskext.babel import lazy_gettext as _
from werkzeug.http import parse_cache_control_header
from molly.apps.common.components import Attribution

class Provider(object):

    def __init__(self, config):
        self._config = config
        self.cache = None
        self.statsd = None

    attribution = Attribution(
        licence_name='Open Government Licence',
        licence_url='http://www.nationalarchives.gov.uk/doc/open-government-licence/',
        attribution_text='Contains public sector information provided by the Met Office'
    )

    def latest_observations(self):
        if self.cache:
            response = self.cache.get(self._CACHE_KEY.format(self._config['location_id']))
        else:
            response = None

        if not response:
            if self.statsd: self.statsd.incr(__name__ + '.cache_miss')

            if self.statsd:
                with self.statsd.timer(__name__ + '.request_time'):
                    response = self._make_request()
            else:
                response = self._make_request()

            max_age = parse_cache_control_header(response.info().getparam('Cache-Control')).max_age

            response = json.load(response)
            if self.cache:
                self.cache.set(
                    self._CACHE_KEY.format(self._config['location_id']),
                    response,
                    max_age
                )
        elif self.statsd:
            self.statsd.incr(__name__ + '.cache_hit')

        source_observation = response['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]
        minutes_since_midnight = timedelta(minutes=int(source_observation['$']))
        obs_time = datetime(
            *time.strptime(response['SiteRep']['DV']['Location']['Period'][-1]['value'], "%Y-%m-%dZ")[:6],
            tzinfo=utc
        )
        obs_time += minutes_since_midnight

        weather_type, weather_type_id = self.WEATHER_TYPES.get(source_observation['W'])

        return {
            'type': weather_type,
            'type_id': weather_type_id,
            'temperature': u'{} °C'.format(source_observation['T']),
            'wind_speed': '{} mph'.format(source_observation['S']),
            'gust_speed': '{} mph'.format(source_observation['G']) if 'G' in source_observation else 'N/A',
            'wind_direction': source_observation['D'],
            'pressure': '{} mb'.format(source_observation['P']),
            'obs_location': capwords(response['SiteRep']['DV']['Location']['name']),
            'obs_time': obs_time.isoformat()
        }

    def _make_request(self):
        return urlopen(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all' +
            '/json/{location_id}?res=hourly&key={api_key}'.format(**self._config)
        )

    _CACHE_KEY = 'weather/metoffice/{}'

    WEATHER_TYPES = {
        'NA': (_('Not available'), ''),
        '0': (_('Clear night'), 'clear_night'),
        '1': (_('Sunny day'), 'sun'),
        '2': (_('Partly cloudy'), 'cloud'),
        '3': (_('Partly cloudy'), 'cloud'),
        '5': (_('Mist'), 'fog'),
        '6': (_('Fog'), 'fog'),
        '7': (_('Cloudy'), 'cloud'),
        '8': (_('Overcast'), 'cloud'),
        '9': (_('Light rain shower'), 'rain'),
        '10': (_('Light rain shower'), 'rain'),
        '11': (_('Drizzle'), 'rain'),
        '12': (_('Light rain'), 'rain'),
        '13': (_('Heavy rain shower'), 'rain'),
        '14': (_('Heavy rain shower'), 'rain'),
        '15': (_('Heavy rain'), 'rain'),
        '16': (_('Sleet shower'), 'rain'),
        '17': (_('Sleet shower'), 'rain'),
        '18': (_('Sleet'), 'rain'),
        '19': (_('Hail shower'), 'rain'),
        '20': (_('Hail shower'), 'rain'),
        '21': (_('Hail'), 'rain'),
        '22': (_('Light snow shower'), 'snow'),
        '23': (_('Light snow shower'), 'snow'),
        '24': (_('Light snow'), 'snow'),
        '25': (_('Heavy snow shower'), 'snow'),
        '26': (_('Heavy snow shower'), 'snow'),
        '27': (_('Heavy snow'), 'snow'),
        '28': (_('Thunder shower'), 'thunder'),
        '29': (_('Thunder shower'), 'thunder'),
        '30': (_('Thunder'), 'thunder')
    }
