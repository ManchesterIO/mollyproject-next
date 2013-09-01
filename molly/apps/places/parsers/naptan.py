import logging
from xml.etree.cElementTree import iterparse
from shapely.geometry import Point

from molly.apps.common.components import Source, Identifier, Attribution
from molly.apps.places.models import PointOfInterest, TIPLOC_NAMESPACE, CRS_NAMESPACE, ATCO_NAMESPACE


LOGGER = logging.getLogger(__name__)

NAPTAN_STOP_TYPES_TO_CATEGORIES = {
    'BCT': 'http://mollyproject.org/poi/types/transport/bus-stop',
    'RLY': 'http://mollyproject.org/poi/types/transport/rail-station',
    'GAT': 'http://mollyproject.org/poi/types/transport/airport',
    'FER': 'http://mollyproject.org/poi/types/transport/ferry-terminal',
    'MET': {
        'AL': 'http://mollyproject.org/poi/types/transport/air-line',
        'AV': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'BB': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'BF': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'BK': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'BL': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'BP': 'http://mollyproject.org/poi/types/transport/tramway-stop',
        'BW': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'BV': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'CA': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'CR':'http://mollyproject.org/poi/types/transport/tramlink-stop',
        'CV': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'CW': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'DF': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'DL': 'http://mollyproject.org/poi/types/transport/dlr-station',
        'DM': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'EB': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'EK': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'EL': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'EV': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'FB': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'FF': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'GC': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'GL': 'http://mollyproject.org/poi/types/transport/subway-station',
        'GO': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'GW': 'http://mollyproject.org/poi/types/transport/gatwick-shuttle-station',
        'GR': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'IW': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'KD': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'KE': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'KW': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'LH': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'LL': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'LU': 'http://mollyproject.org/poi/types/transport/tube-station',
        'MA': 'http://mollyproject.org/poi/types/transport/metrolink-station',
        'MH': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'MN': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'NN': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'NO': 'http://mollyproject.org/poi/types/transport/net-stop',
        'NV': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'NY': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'PD': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'PR': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'RE': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'RH': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SD': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SL': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SM': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SP': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SR': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'ST': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SV': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'SY': 'http://mollyproject.org/poi/types/transport/supertram-stop',
        'TL': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'TW': 'http://mollyproject.org/poi/types/transport/tyne-and-wear-metro-station',
        'TY': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'VR': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'WD': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'WH': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'WL': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'WM': 'http://mollyproject.org/poi/types/transport/midland-metro-stop',
        'WS': 'http://mollyproject.org/poi/types/transport/rail-station/heritage',
        'WW': 'http://mollyproject.org/poi/types/transport/rail-station/heritage'
    },
    'BCS': 'http://mollyproject.org/poi/types/transport/bus-stop',
    'BCQ': 'http://mollyproject.org/poi/types/transport/bus-stop',
    'TXR': 'http://mollyproject.org/poi/types/transport/taxi-rank'
}

class NaptanParser(object):

    _ROOT_ELEM = '{http://www.naptan.org.uk/}NaPTAN'
    _STOP_POINT_ELEM = '{http://www.naptan.org.uk/}StopPoint'

    _STOP_TYPE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}StopType'
    _ATCO_CODE_XPATH = './{http://www.naptan.org.uk/}AtcoCode'
    _CRS_CODE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OffStreet/' \
                      '{http://www.naptan.org.uk/}Rail/{http://www.naptan.org.uk/}AnnotatedRailRef/' \
                      '{http://www.naptan.org.uk/}CrsRef'
    _TIPLOC_CODE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OffStreet/' \
                         '{http://www.naptan.org.uk/}Rail/{http://www.naptan.org.uk/}AnnotatedRailRef/' \
                         '{http://www.naptan.org.uk/}TiplocRef'
    _LONGITUDE_XPATH = './{http://www.naptan.org.uk/}Place/{http://www.naptan.org.uk/}Location/' \
                         '{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Longitude'
    _LATITUDE_XPATH = './{http://www.naptan.org.uk/}Place/{http://www.naptan.org.uk/}Location/' \
                         '{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Latitude'

    _ATTRIBUTION = Attribution(
        attribution_text="Contains public sector information licensed under the Open Government Licence v1.0",
        licence_name='Open Government Licence',
        licence_url='http://www.nationalarchives.gov.uk/doc/open-government-licence/'
    )

    def import_from_file(self, xml_file, source_url):
        self._source_url = source_url
        for event, elem in iterparse(xml_file, events=('start', 'end',)):
            if elem.tag == self._ROOT_ELEM and event == 'start':
                self._source_file = elem.attrib['FileName']

            elif event == 'end' and elem.tag == self._STOP_POINT_ELEM:
                stop_type = self._xpath(elem, self._STOP_TYPE_XPATH)
                if stop_type in NAPTAN_STOP_TYPES_TO_CATEGORIES:
                    yield self._build_point_of_interest(elem, stop_type)

                elem.clear()

    def _build_point_of_interest(self, elem, stop_type):
        poi = PointOfInterest()
        atco_code = self._xpath(elem, self._ATCO_CODE_XPATH)
        poi.slug = 'atco:' + atco_code
        poi.categories.append(self._get_category(stop_type, atco_code))

        poi.identifiers.add(Identifier(namespace=ATCO_NAMESPACE, value=atco_code))
        self._add_identifier(poi, elem, CRS_NAMESPACE, self._CRS_CODE_XPATH)
        self._add_identifier(poi, elem, TIPLOC_NAMESPACE, self._TIPLOC_CODE_XPATH)

        self._add_location(poi, elem)

        poi.sources.append(Source(
            url=self._source_url + '/' + self._source_file,
            version=elem.attrib.get('RevisionNumber', '0'),
            attribution=self._ATTRIBUTION
        ))

        return poi

    def _add_identifier(self, poi, elem, namespace, xpath):
        code_elem = elem.find(xpath)
        if code_elem is not None:
            poi.identifiers.add(Identifier(namespace=namespace, value=code_elem.text))

    def _get_category(self, stop_type, atco_code):
        if stop_type == 'MET':
            subtype = atco_code[6:8]
            category = NAPTAN_STOP_TYPES_TO_CATEGORIES[stop_type].get(subtype)
            if category is None:
                LOGGER.warning('Stop %s has unrecognised MET subtype')
            return category
        else:
            return NAPTAN_STOP_TYPES_TO_CATEGORIES[stop_type]

    def _add_location(self, poi, elem):
        poi.location = Point(
            float(self._xpath(elem, self._LONGITUDE_XPATH)),
            float(self._xpath(elem, self._LATITUDE_XPATH))
        )

    def _xpath(self, elem, xpath):
        return elem.find(xpath).text
