import dateutil.parser
from flask import render_template
from flaskext.babel import gettext as _

from molly.ui.html5.components.component import Component
from molly.ui.html5.components.factory import ComponentFactory

@ComponentFactory.register_component('http://mollyproject.org/apps/weather')
class WeatherHomepage(Component):

    _CSS = frozenset(['style/components/weather/homepage.css'])

    def __init__(self, *args, **kwargs):
        super(WeatherHomepage, self).__init__(*args, **kwargs)
        self._components = map(self._load_component, self._data.get('links', []))

    def render(self):
        return render_template('apps/weather/homepage.html', components=self._components)


@ComponentFactory.register_component('http://mollyproject.org/apps/weather/observation')
class WeatherObservation(Component):

    _CSS = frozenset(['style/components/weather/observation.css'])

    def __init__(self, *args, **kwargs):
        super(WeatherObservation, self).__init__(*args, **kwargs)
        self._context = {
            'href': self.href,
            'weather_type': self._data['observation'].get('type'),
            'weather_type_id': self._data['observation'].get('type_id'),
            'temperature': self._data['observation'].get('temperature'),
            'wind_speed': self._data['observation'].get('wind_speed'),
            'wind_direction': self._data['observation'].get('wind_direction'),
            'gust_speed': self._data['observation'].get('gust_speed'),
            'pressure': self._data['observation'].get('pressure'),
            'observation_location': self._data['observation'].get('obs_location'),
            'observation_time': dateutil.parser.parse(self._data['observation'].get('obs_time')),
            'attribution': self._load_component(self._data.get('attribution'))
        }

    @property
    def title(self):
        return _('Weather at {location}').format(location=self._data['observation'].get('obs_location'))

    def render(self, summary_only=False):
        self._context['summary_only'] = summary_only
        return render_template('apps/weather/observation.html', **self._context)
