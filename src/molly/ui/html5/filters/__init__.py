from molly.ui.html5.filters.phone_number import format_telephone_number
from molly.ui.html5.filters.url import ui_url
from molly.ui.html5.filters.geocoding import reverse_geocode
from molly.ui.html5.filters.humanise import humanise_distance

FILTERS = {
    'format_telephone_number': format_telephone_number,
    'ui_url': ui_url,
    'reverse_geocode': reverse_geocode,
    'humanise_distance': humanise_distance
}
