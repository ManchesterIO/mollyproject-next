# coding=utf-8
from flask import request, render_template
from flask.ext.babel import lazy_gettext as _
from jinja2 import Markup
from molly.apps.places.models import PointOfInterest
from molly.ui.html5.components import ComponentFactory, Component

@ComponentFactory.register_component('http://mollyproject.org/apps/places')
class PlacesHomepage(Component):

    def __init__(self, *args, **kwargs):
        super(PlacesHomepage, self).__init__(*args, **kwargs)
        self._components = map(self._load_component, self._data.get('links', []))

    def render(self):
        return Markup(
            render_template(
                'apps/places/homepage.html',
                components=self._components
            )
        )


@ComponentFactory.register_component('http://mollyproject.org/apps/places/point-of-interest')
class PointOfInterestUI(Component):

    _CSS = frozenset(['style/components/places/point-of-interest.css'])

    def __init__(self, *args, **kwargs):
        super(PointOfInterestUI, self).__init__(*args, **kwargs)
        self._poi = PointOfInterest.from_dict(self._data['poi'])
        self._categories = _CATEGORIES
        self._amenities = _AMENITIES

    @property
    def title(self):
        if self.category is not None:
            return '{name} - {category}'.format(name=self._poi.name(), category=self.category)
        else:
            return self._poi.name()

    @property
    def category(self):
        if self._poi.primary_type in self._CATEGORIES:
            return self._CATEGORIES[self._poi.primary_type]
        for amenity in self._poi.amenities:
            if amenity in self._AMENITIES:
                return self._AMENITIES[amenity]

    def render(self):
        return Markup(
            render_template(
                'apps/places/point-of-interest.html',
                poi=self._poi,
                links=self._data['links'],
                categories=self._categories,
                amenities=self._amenities,
                attributions=[self._load_component(source.attribution._asdict()) for source in self._poi.sources]
            )
        )


@ComponentFactory.register_component('http://mollyproject.org/apps/places/nearby')
class NearbyPlacesUI(Component):

    _CSS = frozenset(['style/components/places/nearby-search.css'])

    def render(self):
        return Markup(
            render_template(
                'apps/places/nearby-search.html',
                href=self.href
            )
        )


_CATEGORIES = {
    'http://mollyproject.org/poi/types/leisure/arts-centre': _('Arts Centre'),
    'http://mollyproject.org/poi/types/retail/bank': _('Bank'),
    'http://mollyproject.org/poi/types/leisure/bar': _('Bar'),
    'http://mollyproject.org/poi/types/leisure/bench': _('Bench'),
    'http://mollyproject.org/poi/transport/parking/bicycle': _('Bicycle Parking'),
    'http://mollyproject.org/poi/types/transport/bicycle-rental': _('Bicycle Rental'),
    'http://mollyproject.org/poi/types/food/cafe': _(u'Café'),
    'http://mollyproject.org/poi/types/leisure/cinema': _('Cinema'),
    'http://mollyproject.org/poi/types/health/doctors': _('GP'),
    'http://mollyproject.org/poi/types/food/fast-food': _('Fast Food outlet'),
    'http://mollyproject.org/poi/types/transport/fuel': _('Petrol Station'),
    'http://mollyproject.org/poi/types/health/hospital': _('Hospital'),
    'http://mollyproject.org/poi/types/leisure/library': _('Library'),
    'http://mollyproject.org/poi/types/retail/marketplace': _('Marketplace'),
    'http://mollyproject.org/poi/types/leisure/museum': _('Museum'),
    'http://mollyproject.org/poi/types/leisure/nightclub': _('Nightclub'),
    'http://mollyproject.org/poi/types/transport/parking/car': _('Car park'),
    'http://mollyproject.org/poi/types/health/pharmacy': _('Pharmacy'),
    'http://mollyproject.org/poi/types/place-of-worship': _('Place of Worship'),
    'http://mollyproject.org/poi/types/police-station': _('Police Station'),
    'http://mollyproject.org/poi/types/retail/post-office': _('Post Office'),
    'http://mollyproject.org/poi/types/leisure/pub': _('Pub'),
    'http://mollyproject.org/poi/types/leisure/punt-hire': _('Punt Hire'),
    'http://mollyproject.org/poi/types/food/restaurant': _('Restaurant'),
    'http://mollyproject.org/poi/types/transport/taxi-rank': _('Taxi Rank'),
    'http://mollyproject.org/poi/types/leisure/theatre': _('Theatre'),
    'http://mollyproject.org/poi/types/leisure/ice-rink': _('Ice rink'),
    'http://mollyproject.org/poi/types/leisure/park': _('Park'),
    'http://mollyproject.org/poi/types/leisure/sports-centre': _('Sports Centre'),
    'http://mollyproject.org/poi/types/place-of-worship/cathedral': _('Cathedral'),
    'http://mollyproject.org/poi/types/place-of-worship/chapel': _('Chapel'),
    'http://mollyproject.org/poi/types/place-of-worship/church': _('Church'),
    'http://mollyproject.org/poi/types/place-of-worship/mandir': _('Mandir'),
    'http://mollyproject.org/poi/types/place-of-worship/synagogue': _('Synagogue'),
    'http://mollyproject.org/poi/types/place-of-worship/mosque': _('Mosque'),
    'http://mollyproject.org/poi/types/leisure/swimming-pool': _('Swimming Pool'),
    'http://mollyproject.org/poi/types/tourist-information': _('Tourist Information')
}

_AMENITIES = {
    'http://mollyproject.org/poi/amenities/atm': _('Cash point'),
    'http://mollyproject.org/poi/amenities/post-box': _('Post box'),
    'http://mollyproject.org/poi/amenities/recycling': _('Recycling'),
    'http://mollyproject.org/poi/amenities/telephone': _('Public telephone'),
    'http://mollyproject.org/poi/amenities/tourist-attraction': _('Tourist Attraction'),
    }