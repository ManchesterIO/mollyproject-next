# coding=utf-8
from datetime import datetime
from mock import Mock, ANY, MagicMock
from pytz import utc
from StringIO import StringIO
import unittest2 as unittest

import molly.apps.weather.providers.metoffice as provider

class MetOfficeTest(unittest.TestCase):

    def setupMockUrlOpen(self, feed):
        provider.urlopen = Mock(return_value=StringIO(feed))
        provider.urlopen.return_value.info = Mock()
        provider.urlopen.return_value.info.return_value.getparam = Mock(
            return_value='public, no-transform, must-revalidate, max-age=123'
        )

    def setUp(self):
        self.setupMockUrlOpen(OBSERVATION_FEED)

        self._provider = provider.Provider({
            'api_key': '12345',
            'location_id': '100'
        })
        self._provider.cache = Mock()
        self._provider.cache.get.return_value = None

        self._provider.statsd = Mock()
        self._provider.statsd.timer = MagicMock()


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
        self._configure_cache_hit()
        self._provider.latest_observations()
        self._provider.cache.get.assert_called_once_with('weather/metoffice/100')
        self.assertFalse(provider.urlopen.called)

    def test_when_cache_hit_counter_incremented(self):
        self._configure_cache_hit()
        self._provider.latest_observations()
        self._provider.statsd.incr.assert_called_once_with('molly.apps.weather.providers.metoffice.cache_hit')

    def test_when_cache_miss_counter_incremented(self):
        self._provider.latest_observations()
        self._provider.statsd.incr.assert_called_once_with('molly.apps.weather.providers.metoffice.cache_miss')

    def test_midnight_form_of_results_are_handled_correctly(self):
        self.setupMockUrlOpen(MIDNIGHT_OBSERVATION_FEED)
        observation = self._provider.latest_observations()
        self.assertEquals({
            'type': 'Clear night',
            'type_id': 'clear_night',
            'temperature': u'1.8 °C',
            'wind_speed': '18 mph',
            'gust_speed': 'N/A',
            'wind_direction': u'ESE',
            'pressure': '1008 mb',
            'obs_location': u'Leek',
            'obs_time': datetime(2013, 3, 4, 23, 0, tzinfo=utc).isoformat()
        }, observation)

    def _configure_cache_hit(self):
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

MIDNIGHT_OBSERVATION_FEED = """
{"SiteRep": {"DV": {"dataDate": "2013-03-04T23:00:00Z", "type": "Obs", "Location": {"name": "LEEK", "i": "3330",
"country": "ENGLAND", "lon": "-1.983", "Period": {"Rep": [{"D": "SE", "P": "1020", "S": "8", "T": "2.4", "W": "2",
"V": "9000", "$": "0"}, {"D": "ESE", "P": "1019", "S": "8", "T": "1.6", "W": "0", "V": "5000", "$": "60"}, {"D": "SE",
"P": "1019", "S": "9", "T": "1.4", "W": "5", "V": "6000", "$": "120"}, {"D": "SE", "P": "1018", "S": "10", "T": "1.1",
"W": "5", "V": "2800", "$": "180"}, {"D": "SE", "P": "1018", "S": "11", "T": "0.5", "W": "5", "V": "4500", "$": "240"},
{"D": "SSE", "P": "1017", "S": "8", "T": "0.4", "W": "8", "V": "9000", "$": "300"}, {"D": "SSE", "P": "1017",
"S": "10", "T": "0.3", "W": "8", "V": "10000", "$": "360"}, {"D": "SE", "G": "22", "P": "1016", "S": "10", "T": "0.5",
"W": "8", "V": "10000", "$": "420"}, {"D": "SE", "P": "1017", "S": "11", "T": "0.4", "W": "8", "V": "4700",
"$": "480"}, {"D": "SE", "P": "1016", "S": "11", "T": "0.8", "W": "8", "V": "4700", "$": "540"}, {"D": "SE",
"P": "1016", "S": "11", "T": "1.5", "W": "8", "V": "5000", "$": "600"}, {"D": "SE", "P": "1015", "S": "8",
"T": "3.0", "W": "7", "V": "5000", "$": "660"}, {"D": "ESE", "P": "1014", "S": "15", "T": "3.3", "W": "1",
"V": "4900", "$": "720"}, {"D": "ESE", "P": "1012", "S": "21", "T": "4.7", "W": "1", "V": "6000", "$": "780"},
{"D": "ESE", "P": "1011", "S": "19", "T": "5.8", "W": "1", "V": "5000", "$": "840"}, {"D": "E", "P": "1010",
"S": "21", "T": "6.1", "W": "1", "V": "6000", "$": "900"}, {"D": "E", "G": "31", "P": "1009", "S": "25", "T": "5.7",
"W": "1", "V": "7000", "$": "960"}, {"D": "E", "G": "31", "P": "1009", "S": "17", "T": "4.2", "W": "1", "V": "5000",
"$": "1020"}, {"D": "E", "G": "31", "P": "1009", "S": "25", "T": "3.1", "W": "1", "V": "4500", "$": "1080"},
{"D": "E", "G": "29", "P": "1009", "S": "25", "T": "2.4", "W": "2", "V": "4200", "$": "1140"}, {"D": "E", "G": "31",
"P": "1009", "S": "21", "T": "2.1", "W": "0", "V": "4000", "$": "1200"}, {"D": "E", "G": "29", "P": "1008",
"S": "22", "T": "2.2", "W": "0", "V": "3600", "$": "1260"}, {"D": "E", "G": "29", "P": "1008", "S": "22",
"T": "2.1", "W": "0", "V": "3800", "$": "1320"}, {"D": "ESE", "P": "1008", "S": "18", "T": "1.8", "W": "0",
"V": "3800", "$": "1380"}], "type": "Day", "value": "2013-03-04Z"}, "lat": "53.133", "continent": "EUROPE"}},
"Wx": {"Param": [{"units": "mph", "name": "G", "$": "Wind Gust"}, {"units": "C", "name": "T", "$": "Temperature"},
{"units": "m", "name": "V", "$": "Visibility"}, {"units": "compass", "name": "D", "$": "Wind Direction"},
{"units": "mph", "name": "S", "$": "Wind Speed"}, {"units": "", "name": "W", "$": "Weather Type"}, {"units": "hpa",
"name": "P", "$": "Pressure"}]}}}
"""