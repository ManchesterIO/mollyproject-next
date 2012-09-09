from xml.etree.cElementTree import iterparse

from tch.source import Source
from tch.stop import Stop, CallingPoint

class NaptanParser(object):

    _ROOT_ELEM = '{http://www.naptan.org.uk/}NaPTAN'
    _STOP_POINT_ELEM = '{http://www.naptan.org.uk/}StopPoint'

    _STOP_TYPE_XPATH = './{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}StopType'
    _ATCO_CODE_XPATH = './{http://www.naptan.org.uk/}AtcoCode'

    _LICENCE = "Open Government Licence"
    _LICENCE_URL = "http://www.nationalarchives.gov.uk/doc/open-government-licence/"
    _ATTRIBUTION = "Contains public sector information licensed under the Open Government Licence v1.0"

    def import_from_file(self, file, source_url):
        self._source_url = source_url
        for event, elem in iterparse(file, events=('start', 'end',)):
            if elem.tag == self._ROOT_ELEM and event == 'start':
                self._source_file = elem.attrib['FileName']

            elif event == 'end':
                if elem.tag == self._STOP_POINT_ELEM:
                    stop_type = elem.find(self._STOP_TYPE_XPATH).text

                    if stop_type == 'BCT':
                        bus_stop, calling_point = self._build_bus_stop(elem)
                        yield bus_stop
                        yield calling_point
                        elem.clear()

    def _build_bus_stop(self, elem):
        stop = Stop()
        calling_point = CallingPoint()

        atco_code = elem.find(self._ATCO_CODE_XPATH).text

        sources = [Source(
            url=self._source_url + '/' + self._source_file,
            version=elem.attrib['RevisionNumber'],
            licence=self._LICENCE,
            licence_url=self._LICENCE_URL,
            attribution=self._ATTRIBUTION
        )]
        stop.sources = sources
        calling_point.sources = sources

        stop.url = '/gb/' + atco_code
        calling_point.url = '/gb/' + atco_code + '/calling_point'

        stop.calling_points = [calling_point.url]
        calling_point.parent_stop = stop.url

        return stop, calling_point
