from xml.etree.ElementTree import iterparse
from tch.identifier import Identifier
from tch.locality import Locality, NPTG_REGION_CODE_NAMESPACE
from tch.source import Source

class NptgParser(object):

    _ROOT_ELEM = '{http://www.naptan.org.uk/}NationalPublicTransportGazetteer'
    _REGION_ELEM = '{http://www.naptan.org.uk/}Region'
    _DISTRICT_ELEM = '{http://www.naptan.org.uk/}NptgDistrict'
    _LOCALITY_ELEM = '{http://www.naptan.org.uk/}NptgLocality'

    _REGION_CODE_ELEM = '{http://www.naptan.org.uk/}RegionCode'

    def import_from_file(self, file, source_url):
        self._source_url = source_url
        for event, elem in iterparse(file, events=('start', 'end',)):

            if elem.tag == self._ROOT_ELEM and event == 'start':
                self._source_file = elem.attrib['FileName']

            elif event == 'end':
                handler = {
                    self._REGION_ELEM: self._build_region,
                    self._DISTRICT_ELEM: self._build_locality,
                    self._LOCALITY_ELEM: self._build_locality
                }.get(elem.tag)

                if handler:
                    yield handler(elem)
                    elem.clear()

    def _build_locality(self, elem):
        locality = Locality()
        locality.sources = [
            Source(url=self._source_url + "/" + self._source_file,
                version=elem.attrib['RevisionNumber'])
        ]
        return locality

    def _build_region(self, elem):
        locality = self._build_locality(elem)
        region_code = elem.find(self._REGION_CODE_ELEM).text

        locality.url = "/" + region_code + "/"
        locality.identifiers = [
            Identifier(namespace=NPTG_REGION_CODE_NAMESPACE, value=region_code)
        ]

        return locality