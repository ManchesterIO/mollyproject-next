# coding=utf-8
from operator import itemgetter
from flask import request, render_template
from flask.ext.babel import lazy_gettext as _
from jinja2 import Markup
from shapely.geometry import asShape
from molly.apps.places.models import PointOfInterest
from molly.ui.html5.components import ComponentFactory, Component
from molly.ui.html5.filters import reverse_geocode


class PlacesComponent(Component):

    def _get_human_category(self, category, plural=False):
        return _CATEGORIES.get(category, (_("Unknown category"),))[1 if plural else 0]

    def _get_human_amenity(self, amenity, plural=False):
        return _AMENITIES.get(amenity, (_("Unknown facility"),))[1 if plural else 0]


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
            return self._CATEGORIES[self._poi.primary_type][0]
        for amenity in self._poi.amenities:
            if amenity in self._AMENITIES:
                return self._AMENITIES[amenity][0]

    def render(self, link_only=False):
        if link_only:
            template = 'apps/places/point-of-interest-link.html'
        else:
            template = 'apps/places/point-of-interest.html'
        return Markup(
            render_template(
                template,
                href=self.href,
                poi=self._poi,
                links=self._data.get('links', []),
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


@ComponentFactory.register_component('http://mollyproject.org/apps/places/categories')
class CategoryListUI(PlacesComponent):

    def __init__(self, data, component_factory):
        super(CategoryListUI, self).__init__(data, component_factory)
        self._point = asShape(data['location_filter']['centre'])

    @property
    def title(self):
        return _('Points of Interest near to %(location)s', location=reverse_geocode(self._point))

    def render(self):
        return Markup(
            render_template(
                'apps/places/category-list.html',
                within=self._data['location_filter']['within'],
                centre_point=self._point,
                categories=[
                    self._load_component(category) for category in sorted(
                        self._data['categories'],
                        key=lambda data: self._get_human_category(data['category'])
                    )
                ],
                amenities=[
                    self._load_component(category) for category in sorted(
                        self._data['amenities'],
                        key=lambda data: self._get_human_amenity(data['amenity'])
                    )
                ]
            )
        )


class PointOfInterestListUI(PlacesComponent):

    def __init__(self, data, component_factory):
        super(PointOfInterestListUI, self).__init__(data, component_factory)
        self._point = asShape(data['location_filter']['centre'])

    def render(self):
        if 'href' in self._data:
            template, context = self._render_link()
        else:
            template, context = self._render_list()
        context['CATEGORIES'] = _CATEGORIES
        context['AMENITIES'] = _AMENITIES
        return Markup(
            render_template(
                template,
                **context
            )
        )

    def _render_link(self):
        context = {'href': self.href}
        context.update(self._data)
        template = 'apps/places/point-of-interest-list-link.html'
        return template, context

    def _render_list(self):
        context = {
            'pois': [self._load_component(poi) for poi in self._data['points_of_interest']]
        }
        template = 'apps/places/point-of-interest-list.html'
        return template, context




@ComponentFactory.register_component('http://mollyproject.org/apps/places/points-of-interest/by-category')
class ByCategoryPointOfInterestListUI(PointOfInterestListUI):

    @property
    def title(self):
        return _(
            '%(category)s near %(location)s',
            category=self._get_human_category(self._data['category']),
            location=reverse_geocode(self._point)
        )


@ComponentFactory.register_component('http://mollyproject.org/apps/places/points-of-interest/by-amenity')
class ByAmenityPointOfInterestListUI(PointOfInterestListUI):

    @property
    def title(self):
        return _(
            '%(amenity)s near %(location)s',
            category=self._get_human_amenity(self._data['amenity']),
            location=reverse_geocode(self._point)
        )


_CATEGORIES = {
    'http://mollyproject.org/poi/types/leisure/arts-centre': (_('Arts Centre'), _('Art Centres')),
    'http://mollyproject.org/poi/types/retail/bank': (_('Bank'), _('Banks')),
    'http://mollyproject.org/poi/types/leisure/bar': (_('Bar'), _('Bars')),
    'http://mollyproject.org/poi/types/leisure/bench': (_('Bench'), _('Benches')),
    'http://mollyproject.org/poi/transport/parking/bicycle': (_('Bicycle Parking'), _('Bicycle Parking')),
    'http://mollyproject.org/poi/types/transport/bicycle-rental': (_('Bicycle Rental'), _('Bicycle Rental')),
    'http://mollyproject.org/poi/types/food/cafe': (_(u'Café'), _(u'Cafés')),
    'http://mollyproject.org/poi/types/leisure/cinema': (_('Cinema'), _('Cinemas')),
    'http://mollyproject.org/poi/types/health/doctors': (_('GP'), _('GP surgeries')),
    'http://mollyproject.org/poi/types/food': (_('Food outlet'), _('Food outlets')),
    'http://mollyproject.org/poi/types/food/fast-food': (_('Fast Food outlet'), _('Fast Food outlets')),
    'http://mollyproject.org/poi/types/transport/fuel': (_('Petrol Station'), _('Petrol stations')),
    'http://mollyproject.org/poi/types/health': (_('Healthcare'), _('Healthcase')),
    'http://mollyproject.org/poi/types/health/hospital': (_('Hospital'), _('Hospitals')),
    'http://mollyproject.org/poi/types/leisure/library': (_('Library'), _('Libraries')),
    'http://mollyproject.org/poi/types/retail/marketplace': (_('Marketplace'), _('Marketplaces')),
    'http://mollyproject.org/poi/types/leisure/museum': (_('Museum'), _('Museums')),
    'http://mollyproject.org/poi/types/leisure/nightclub': (_('Nightclub'), _('Nightclubs')),
    'http://mollyproject.org/poi/types/transport/parking/car': (_('Car park'), _('Car parks')),
    'http://mollyproject.org/poi/types/health/pharmacy': (_('Pharmacy'), _('Pharmacies')),
    'http://mollyproject.org/poi/types/place-of-worship': (_('Place of Worship'), _('Places of Worship')),
    'http://mollyproject.org/poi/types/police-station': (_('Police Station'), _('Police Stations')),
    'http://mollyproject.org/poi/types/retail/post-office': (_('Post Office'), _('Post Offices')),
    'http://mollyproject.org/poi/types/leisure/pub': (_('Pub'), _('Pubs')),
    'http://mollyproject.org/poi/types/leisure/punt-hire': (_('Punt Hire'), _('Punt Hire')),
    'http://mollyproject.org/poi/types/food/restaurant': (_('Restaurant'), _('Restaurants')),
    'http://mollyproject.org/poi/types/transport/taxi-rank': (_('Taxi Rank'), _('Taxi Ranks')),
    'http://mollyproject.org/poi/types/leisure/theatre': (_('Theatre'), _('Theatres')),
    'http://mollyproject.org/poi/types/leisure/ice-rink': (_('Ice Rink'), _('Ice Rinks')),
    'http://mollyproject.org/poi/types/leisure/park': (_('Park'), _('Parks')),
    'http://mollyproject.org/poi/types/leisure/sports-centre': (_('Sports Centre'), _('Sports Centres')),
    'http://mollyproject.org/poi/types/place-of-worship/cathedral': (_('Cathedral'), _('Cathedral')),
    'http://mollyproject.org/poi/types/place-of-worship/chapel': (_('Chapel'), _('Chapels')),
    'http://mollyproject.org/poi/types/place-of-worship/church': (_('Church'), _('Churches')),
    'http://mollyproject.org/poi/types/place-of-worship/mandir': (_('Hindu Temple'), _('Hindu Temples')),
    'http://mollyproject.org/poi/types/place-of-worship/synagogue': (_('Synagogue'), _('Synagogues')),
    'http://mollyproject.org/poi/types/place-of-worship/mosque': (_('Mosque'), _('Mosques')),
    'http://mollyproject.org/poi/types/leisure/swimming-pool': (_('Swimming Pool'), _('Swimming Pools')),
    'http://mollyproject.org/poi/types/tourist-information': (_('Tourist Information'), _('Tourist Information')),
    'http://mollyproject.org/poi/types/transport/bus-stop': (_('Bus Stop'), _('Bus Tops')),
    'http://mollyproject.org/poi/types/transport/rail-station': (_('Rail Station'), _('Rail Stations')),
    'http://mollyproject.org/poi/types/transport/airport': (_('Airport'), _('Airports')),
    'http://mollyproject.org/poi/types/transport/ferry-terminal': (_('Port'), _('Ports')),
    'http://mollyproject.org/poi/types/transport/air-line': (_('Emirates Air Line'), _('Emirates Air Line')),
    'http://mollyproject.org/poi/types/transport/tramway-stop': (_('Tramway Stop'), _('Tramway Stops')),
    'http://mollyproject.org/poi/types/transport/tramlink-stop': (_('Tramlink Stop'), _('Tramlink Stops')),
    'http://mollyproject.org/poi/types/transport/dlr-station': (_('DLR Station'), _('DLR Stations')),
    'http://mollyproject.org/poi/types/transport/subway-station': (_('Subway Station'), _('Subway Stations')),
    'http://mollyproject.org/poi/types/transport/gatwick-shuttle-station': (_('Gatwick Shuttle Station'), _('Gatwick Shuttle Stations')),
    'http://mollyproject.org/poi/types/transport/tube-station': (_('Tube Station'), _('Tube Stations')),
    'http://mollyproject.org/poi/types/transport/metrolink-station': (_('Metrolink Station'), _('Metrolink Stations')),
    'http://mollyproject.org/poi/types/transport/net-stop': (_('NET Stop'), _('NET Stops')),
    'http://mollyproject.org/poi/types/transport/supertram-stop': (_('Supertram Stop'), _('Supertram Stops')),
    'http://mollyproject.org/poi/types/transport/tyne-and-wear-metro-station': (_('Metro Station'), _('Metro Stations')),
    'http://mollyproject.org/poi/types/transport/midland-metro-stop': (_('Metro Stop'), _('Metro Stops')),
    'http://mollyproject.org/poi/types/transport/rail-station/heritage': (_('Heritage Railway'), _('Heritage Railways'))
}

_AMENITIES = {
    'http://mollyproject.org/poi/amenities/atm': (_('Cash Point'), _('Cash Points')),
    'http://mollyproject.org/poi/amenities/post-box': (_('Post Box'), _('Post Boxes')),
    'http://mollyproject.org/poi/amenities/recycling': (_('Recycling'), _('Recycling')),
    'http://mollyproject.org/poi/amenities/telephone': (_('Public Telephone'), _('Public Telephones')),
    'http://mollyproject.org/poi/amenities/tourist-attraction': (_('Tourist Attraction'), _('Tourist Attractions'))
}