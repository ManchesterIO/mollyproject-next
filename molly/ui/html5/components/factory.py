from molly.ui.html5.components.common import Attribution
from molly.ui.html5.components.component import Component
from molly.ui.html5.components.homepage import Homepage
from molly.ui.html5.components.weather import WeatherObservation, WeatherHomepage

class ComponentFactory(object):

    _COMPONENTS = {
        'http://mollyproject.org/apps/homepage': Homepage,
        'http://mollyproject.org/common/attribution': Attribution,
        'http://mollyproject.org/apps/weather': WeatherHomepage,
        'http://mollyproject.org/apps/weather/observation': WeatherObservation
    }

    def __call__(self, obj):
        return self._COMPONENTS.get(obj['self'], Component)(obj, self)
