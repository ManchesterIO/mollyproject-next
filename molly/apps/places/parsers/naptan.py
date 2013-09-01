from xml.etree.cElementTree import iterparse

from molly.apps.common.components import Source, Identifier, Attribution
from molly.apps.places.models import PointOfInterest, TIPLOC_NAMESPACE, CRS_NAMESPACE, ATCO_NAMESPACE

NAPTAN_STOP_TYPES_TO_CATEGORIES = {
    'BCT': 'http://mollyproject.org/poi/types/transport/bus-stop',
    'RLY': 'http://mollyproject.org/poi/types/transport/rail-station',
    'GAT': 'http://mollyproject.org/poi/types/transport/airport',
    'FER': 'http://mollyproject.org/poi/types/transport/ferry-terminal',
    'MET': 'http://mollyproject.org/poi/types/transport/metro-station',
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
                stop_type = elem.find(self._STOP_TYPE_XPATH).text

                # BCT: Bus Stop, RLY: Railway Station
                # GAT: Airport/terminal
                # FER: Ferry port, MET: Metro station
                # BCS: Marked bus station bay, BCQ: Variable bus station bay
                # TXR: Taxi Rank
                if stop_type in NAPTAN_STOP_TYPES_TO_CATEGORIES:
                    yield self._build_point_of_interest(elem, NAPTAN_STOP_TYPES_TO_CATEGORIES[stop_type])

                elem.clear()

    def _build_point_of_interest(self, elem, category):
        poi = PointOfInterest()
        poi.sources.append(Source(
            url=self._source_url + '/' + self._source_file,
            version=elem.attrib.get('RevisionNumber', '0'),
            attribution=self._ATTRIBUTION
        ))
        poi.categories.append(category)
        atco_code = self._get_atco_code(elem)
        poi.slug = 'atco:' + atco_code
        poi.identifiers.add(Identifier(namespace=ATCO_NAMESPACE, value=atco_code))

        self._add_identifier(poi, elem, CRS_NAMESPACE, self._CRS_CODE_XPATH)
        self._add_identifier(poi, elem, TIPLOC_NAMESPACE, self._TIPLOC_CODE_XPATH)

        return poi

    def _get_atco_code(self, elem):
        return elem.find(self._ATCO_CODE_XPATH).text

    def _add_identifier(self, poi, elem, namespace, xpath):
        code_elem = elem.find(xpath)
        if code_elem is not None:
            poi.identifiers.add(Identifier(namespace=namespace, value=code_elem.text))
