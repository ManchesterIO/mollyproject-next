from collections import defaultdict
from xml.etree.cElementTree import iterparse
from tch.identifier import Identifier

from tch.source import Source
from tch.stop import Stop, CallingPoint, ATCO_NAMESPACE, CRS_NAMESPACE, TIPLOC_NAMESPACE

class NaptanParser(object):

    _ROOT_ELEM = '{http://www.naptan.org.uk/}NaPTAN'
    _STOP_POINT_ELEM = '{http://www.naptan.org.uk/}StopPoint'

    _STOP_TYPE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}StopType'
    _ATCO_CODE_XPATH = './{http://www.naptan.org.uk/}AtcoCode'
    _STOP_AREA_REF_XPATH = './{http://www.naptan.org.uk/}StopAreas/{http://www.naptan.org.uk/}StopAreaRef'
    _CRS_CODE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OffStreet/' \
                      '{http://www.naptan.org.uk/}Rail/{http://www.naptan.org.uk/}AnnotatedRailRef/' \
                      '{http://www.naptan.org.uk/}CrsRef'
    _TIPLOC_CODE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OffStreet/' \
                         '{http://www.naptan.org.uk/}Rail/{http://www.naptan.org.uk/}AnnotatedRailRef/' \
                         '{http://www.naptan.org.uk/}TiplocRef'

    _LICENCE = "Open Government Licence"
    _LICENCE_URL = "http://www.nationalarchives.gov.uk/doc/open-government-licence/"
    _ATTRIBUTION = "Contains public sector information licensed under the Open Government Licence v1.0"

    def import_from_file(self, file, source_url):
        self._airports = dict()
        self._stations = defaultdict(list)
        self._calling_points = dict()
        self._source_url = source_url
        for event, elem in iterparse(file, events=('start', 'end',)):
            if elem.tag == self._ROOT_ELEM and event == 'start':
                self._source_file = elem.attrib['FileName']

            elif event == 'end':
                if elem.tag == self._STOP_POINT_ELEM:
                    stop_type = elem.find(self._STOP_TYPE_XPATH).text

                    # BCT: Bus Stop, RLY: Railway Station
                    if stop_type in ('BCT', 'RLY'):
                        stop, calling_point = self._build_stop_with_calling_point(elem)
                        yield stop
                        yield calling_point

                    # GAT: Airport/terminal
                    elif stop_type == 'GAT':
                        self._build_airport(elem)

                    # FER: Ferry port, MET: Metro station
                    elif stop_type in ('FER', 'MET'):
                        stop, calling_point, group = self._build_station(elem)
                        self._stations[group] = [stop]
                        self._calling_points[group] = calling_point

                    # FBT: Ferry berth, PLT: Metro platform
                    elif stop_type in ('FBT', 'PLT'):
                        calling_point, group = self._build_calling_point(elem)
                        self._stations[group].append(calling_point)

                    # BCS: Marked bus station bay, BCQ: Variable bus station bay
                    elif stop_type in ('BCS', 'BCQ'):
                        bay, stop = self._build_bus_station(elem)
                        yield bay
                        yield stop

                    elem.clear()

        for airport in self._airports.values():
            yield airport

        for group, calling_points in self._stations.iteritems():
            parent = calling_points[0]
            if len(calling_points) == 1:
                yield self._calling_points[group]
            else:
                parent.calling_points.remove(self._calling_points[group].url)

            for calling_point in calling_points[1:]:
                parent.calling_points.add(calling_point.url)
                calling_point.parent_stop = parent.url
                yield calling_point

            yield parent


    def _build_stop_with_calling_point(self, elem):
        stop = self._build_base(elem)

        calling_point = CallingPoint()
        calling_point.sources = stop.sources
        calling_point.url = stop.url + '/calling_point'

        stop.calling_points = {calling_point.url}
        calling_point.parent_stop = stop.url

        return stop, calling_point

    def _build_airport(self, elem):
        atco_code = self._get_atco_code(elem)
        # This assumes that the main airport element is the same code except with
        # 0 at the end (this is true in the current NaPTAN dump)
        parent_atco_code = atco_code[:-1] + '0'

        # This makes the assumption that the complete airport is seen before any
        # of the terminals - this is true in the current version of the NaPTAN dump
        is_terminal = parent_atco_code in self._airports.keys()
        airport = self._build_base(elem, CallingPoint if is_terminal else Stop)
        if is_terminal:
            airport.parent_stop = '/gb/' + parent_atco_code
            calling_point_url = self._airports[parent_atco_code].url + '/calling_point'
            if calling_point_url in self._airports:
                self._airports[parent_atco_code].calling_points.remove(calling_point_url)
                del self._airports[calling_point_url]
            self._airports[parent_atco_code].calling_points.add(airport.url)
        else:
            calling_point = self._build_base(elem, CallingPoint)
            calling_point.url += '/calling_point'
            calling_point.parent_url = airport.url
            airport.calling_points.add(calling_point.url)
            self._airports[calling_point.url] = calling_point

        self._airports[atco_code] = airport

    def _build_station(self, elem):
        stop, calling_point = self._build_stop_with_calling_point(elem)
        group = self._get_group_id(elem, False)

        return stop, calling_point, group

    def _build_calling_point(self, elem):
        calling_point = self._build_base(elem, CallingPoint)
        group = self._get_group_id(elem, True)

        return calling_point, group

    def _build_bus_station(self, elem):
        bay = self._build_base(elem, CallingPoint)
        stop = self._build_base(elem, Stop)
        stop.url += '/bus_station'
        bay.parent_url = stop.url
        stop.calling_points.add(bay.url)
        return bay, stop

    def _get_group_id(self, elem, elem_is_child):
        group_elem = elem.find(self._STOP_AREA_REF_XPATH)
        if group_elem is not None:
            group = group_elem.text
        else:
            group = self._get_atco_code(elem)
            group = group[:3] + 'G' + group[4:]
            if elem_is_child: group = group[:-1]
        return group

    def _build_base(self, elem, point_type=Stop):
        point = point_type()
        point.sources.add(Source(
            url=self._source_url + '/' + self._source_file,
            version=elem.attrib.get('RevisionNumber', '0'),
            licence=self._LICENCE,
            licence_url=self._LICENCE_URL,
            attribution=self._ATTRIBUTION
        ))
        atco_code = self._get_atco_code(elem)
        point.url = '/gb/' + atco_code
        point.identifiers.add(Identifier(namespace=ATCO_NAMESPACE, value=atco_code))

        self._add_identifier(point, elem, CRS_NAMESPACE, self._CRS_CODE_XPATH)
        self._add_identifier(point, elem, TIPLOC_NAMESPACE, self._TIPLOC_CODE_XPATH)

        return point

    def _get_atco_code(self, elem):
        return elem.find(self._ATCO_CODE_XPATH).text

    def _add_identifier(self, point, elem, namespace, xpath):
        code_elem = elem.find(xpath)
        if code_elem is not None:
            point.identifiers.add(Identifier(namespace=namespace, value=code_elem.text))
