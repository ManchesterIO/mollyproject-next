# coding=utf-8
from datetime import datetime
from mock import Mock, ANY
from pytz import utc
from StringIO import StringIO
import unittest2 as unittest

import molly.apps.weather.providers.metoffice as provider

class MetOfficeTest(unittest.TestCase):

    def setUp(self):
        provider.urlopen = Mock(return_value=StringIO(OBSERVATION_FEED))
        provider.urlopen.return_value.info = Mock()
        provider.urlopen.return_value.info.return_value.getparam = Mock(
            return_value='public, no-transform, must-revalidate, max-age=123'
        )

        self._provider = provider.Provider({
            'api_key': '12345',
            'location_id': '100'
        })
        self._provider.cache = Mock()
        self._provider.cache.get.return_value = None


    def test_met_office_hits_correct_endpoint(self):
        self._provider.latest_observations()

        provider.urlopen.assert_called_once_with(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/100?res=hourly&key=12345'
        )

    def test_observations_are_parsed_correctly(self):
        observation = self._provider.latest_observations()
        self.assertEquals({
            'type': 'Partly cloudy',
            'type_id': 'cloud',
            'temperature': u'16.3 °C',
            'wind_speed': '18 mph',
            'gust_speed': 'N/A',
            'wind_direction': u'SW',
            'pressure': '1016 mb',
            'obs_location': u'Heathrow',
            'obs_time': datetime(2012, 9, 30, 16, 0, tzinfo=utc).isoformat()
        }, observation)

    def test_provider_shows_correct_attribution(self):
        self.assertEquals(
            'Open Government Licence',
            self._provider.attribution.licence_name
        )
        self.assertEquals(
            'http://www.nationalarchives.gov.uk/doc/open-government-licence/',
            self._provider.attribution.licence_url
        )
        self.assertEquals(
            'Contains public sector information provided by the Met Office',
            self._provider.attribution.attribution_text
        )

    def test_max_age_is_used_to_populate_cache(self):
        provider.urlopen.return_value.info.return_value.getparam = Mock(
            return_value='public, no-transform, must-revalidate, max-age=123'
        )

        self._provider.latest_observations()
        self._provider.cache.set.assert_called_once_with('weather/metoffice/100', ANY, 123)

    def test_when_cache_exists_urlopen_is_not_hit(self):
        self._provider.cache.get.return_value = {
            'SiteRep': {
                'DV': {
                    'Location': {
                        'Period': [{
                                       'Rep': [{u'$': u'0',
                                                 u'D': u'W',
                                                 u'P': u'1022',
                                                 u'S': u'5',
                                                 u'T': u'7.8',
                                                 u'V': u'18000',
                                                 u'W': u'0'
                                               }],
                                       'value': '2012-09-29Z'}],
                        'name': 'Foo'
                    }
                }
            }
        }
        self._provider.latest_observations()
        self._provider.cache.get.assert_called_once_with('weather/metoffice/100')
        self.assertFalse(provider.urlopen.called)


OBSERVATION_FEED = """
{"SiteRep":{"Wx":{"Param":[{"name":"F","units":"","$":"Feels Like Temperature"},
{"name":"G","units":"mph","$":"Wind Gust"},{"name":"H","units":"%","$":"Screen Relative Humidity"},
{"name":"T","units":"C","$":"Temperature"},{"name":"V","units":"m","$":"Visibility"},
{"name":"D","units":"compass","$":"Wind Direction"},{"name":"S","units":"mph","$":"Wind Speed"},
{"name":"U","units":"","$":"Max UV Index"},{"name":"W","units":"","$":"Weather Type"},
{"name":"Pp","units":"","$":"Precipitation Probability"},{"name":"P","units":"hpa","$":"Pressure"}]},
"DV":{"dataDate":"2012-09-30T16:00:00Z","type":"Obs","Location":{"i":"3772","lat":"51.479","lon":"-0.449",
"name":"HEATHROW","country":"ENGLAND","continent":"EUROPE","Period":[{"type":"Day","value":"2012-09-29Z",
"Rep":[{"D":"W","P":"1019","S":"9","T":"14.8","V":"27000","W":"3","$":"960"},{"D":"WNW","P":"1019",
"S":"8","T":"14.5","V":"22000","W":"3","$":"1020"},{"D":"W","P":"1020","S":"6","T":"13.5","V":"25000",
"W":"1","$":"1080"},{"D":"W","P":"1020","S":"6","T":"12.3","V":"21000","W":"0","$":"1140"},{"D":"W",
"P":"1021","S":"7","T":"11.9","V":"20000","W":"0","$":"1200"},{"D":"W","P":"1021","S":"7","T":"10.5",
"V":"17000","W":"0","$":"1260"},{"D":"W","P":"1021","S":"6","T":"10.1","V":"20000","W":"0","$":"1320"},
{"D":"W","P":"1021","S":"5","T":"8.2","V":"19000","W":"0","$":"1380"}]},{"type":"Day","value":"2012-09-30Z",
"Rep":[{"D":"W","P":"1022","S":"5","T":"7.8","V":"18000","W":"0","$":"0"},{"D":"W","P":"1021","S":"7",
"T":"7.7","V":"18000","W":"0","$":"60"},{"D":"W","P":"1021","S":"5","T":"7.6","V":"17000","W":"0","$":"120"},
{"D":"WSW","P":"1021","S":"3","T":"6.5","V":"15000","W":"0","$":"180"},{"D":"SW","P":"1020","S":"5","T":"6.9",
"V":"15000","W":"0","$":"240"},{"D":"SSW","P":"1020","S":"9","T":"7.5","V":"15000","W":"0","$":"300"},
{"D":"SSW","P":"1019","S":"11","T":"7.8","V":"16000","W":"1","$":"360"},{"D":"SSW","P":"1020","S":"13","T":
"9.6","V":"19000","W":"7","$":"420"},{"D":"SSW","P":"1020","S":"10","T":"10.3","V":"19000","W":"1","$":"480"},
{"D":"SW","P":"1020","S":"9","T":"13.0","V":"20000","W":"3","$":"540"},{"D":"WSW","G":"29","P":"1019","S":"16",
"T":"14.4","V":"24000","W":"7","$":"600"},{"D":"SW","P":"1019","S":"16","T":"15.2","V":"25000","W":"7","$":"660"},
{"D":"WSW","G":"31","P":"1019","S":"19","T":"16.7","V":"25000","W":"7","$":"720"},{"D":"SW","P":"1018","S":"19",
"T":"16.9","V":"25000","W":"7","$":"780"},{"D":"SW","P":"1017","S":"18","T":"17.3","V":"28000","W":"8","$":"840"},
{"D":"SW","P":"1017","S":"16","T":"16.8","V":"24000","W":"8","$":"900"},{"D":"SW","P":"1016","S":"18","T":"16.3",
"V":"22000","W":"3","$":"960"}]}]}}}}
"""
