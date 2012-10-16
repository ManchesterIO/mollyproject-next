# coding=utf-8
from datetime import timedelta, datetime
import json
from string import capwords
from pytz import utc
import time
from urllib2 import urlopen

from flaskext.babel import lazy_gettext as _
from molly.apps.common.attribution import Attribution

class Provider(object):

    def __init__(self, config):
        self._config = config

    attribution = Attribution(
        licence_name='Open Government Licence',
        licence_url='http://www.nationalarchives.gov.uk/doc/open-government-licence/',
        attribution_text='Contains public sector information provided by the Met Office'
    )

    def latest_observations(self):
        response = json.load(
            urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all' +
                '/json/{location_id}?res=hourly&key={api_key}'.format(**self._config))
        )

        source_observation = response['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]
        minutes_since_midnight = timedelta(minutes=int(source_observation['$']))
        obs_time = datetime(
            *time.strptime(response['SiteRep']['DV']['Location']['Period'][-1]['value'], "%Y-%m-%dZ")[:6],
            tzinfo=utc
        )
        obs_time += minutes_since_midnight

        return {
            'type': self.WEATHER_TYPES.get(source_observation['W']),
            'temperature': u'{} °C'.format(source_observation['T']),
            'wind_speed': '{} mph'.format(source_observation['S']),
            'gust_speed': '{} mph'.format(source_observation['G']) if 'G' in source_observation else 'N/A',
            'wind_direction': source_observation['D'],
            'pressure': '{} mb'.format(source_observation['P']),
            'obs_location': capwords(response['SiteRep']['DV']['Location']['name']),
            'obs_time': obs_time.isoformat()
        }

    WEATHER_TYPES = {
        'NA': _('Not available'),
        '0': _('Clear night'),
        '1': _('Sunny day'),
        '2': _('Partly cloudy'),
        '3': _('Partly cloudy'),
        '4': _('Not used'),
        '5': _('Mist'),
        '6': _('Fog'),
        '7': _('Cloudy'),
        '8': _('Overcast'),
        '9': _('Light rain shower'),
        '10': _('Light rain shower'),
        '11': _('Drizzle'),
        '12': _('Light rain'),
        '13': _('Heavy rain shower'),
        '14': _('Heavy rain shower'),
        '15': _('Heavy rain'),
        '16': _('Sleet shower'),
        '17': _('Sleet shower'),
        '18': _('Sleet'),
        '19': _('Hail shower'),
        '20': _('Hail shower'),
        '21': _('Hail'),
        '22': _('Light snow shower'),
        '23': _('Light snow shower'),
        '24': _('Light snow'),
        '25': _('Heavy snow shower'),
        '26': _('Heavy snow shower'),
        '27': _('Heavy snow'),
        '28': _('Thunder shower'),
        '29': _('Thunder shower'),
        '30': _('Thunder')
    }
