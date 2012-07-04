from xml.etree.ElementTree import iterparse
from tch.identifier import Identifier
from tch.locality import Locality, NPTG_REGION_CODE_NAMESPACE, NPTG_DISTRICT_CODE_NAMESPACE, \
    NPTG_LOCALITY_CODE_NAMESPACE
from tch.source import Source

class NptgParser(object):

    _ROOT_ELEM = '{http://www.naptan.org.uk/}NationalPublicTransportGazetteer'
    _REGION_ELEM = '{http://www.naptan.org.uk/}Region'
    _LOCALITY_ELEM = '{http://www.naptan.org.uk/}NptgLocality'

    _LANGUAGE_ATTRIB = '{http://www.w3.org/XML/1998/namespace}lang'

    _DISTRICT_XPATH = './/{http://www.naptan.org.uk/}NptgDistrict'
    _REGION_CODE_XPATH = './{http://www.naptan.org.uk/}RegionCode'
    _REGION_DISTRICT_NAME_XPATH = './{http://www.naptan.org.uk/}Name'
    _DISTRICT_CODE_XPATH = './{http://www.naptan.org.uk/}NptgDistrictCode'
    _LOCALITY_CODE_XPATH = './{http://www.naptan.org.uk/}NptgLocalityCode'

    def import_from_file(self, file, source_url):
        self._source_url = source_url
        for event, elem in iterparse(file, events=('start', 'end',)):
            if elem.tag == self._ROOT_ELEM and event == 'start':
                self._source_file = elem.attrib['FileName']

            elif event == 'end':
                if elem.tag == self._REGION_ELEM:
                    for locality in self._build_region(elem):
                        yield locality
                    elem.clear()
                elif elem.tag == self._LOCALITY_ELEM:
                    yield self._build_locality(elem)

    def _build_base_locality(self, elem):
        locality = Locality()
        locality.sources = [
            Source(url=self._source_url + "/" + self._source_file, version=elem.attrib['RevisionNumber'])
        ]
        return locality

    def _build_region(self, elem):
        locality = self._build_base_locality(elem)
        region_code = elem.find(self._REGION_CODE_XPATH).text

        locality.url = "/" + region_code
        locality.identifiers = [
            Identifier(namespace=NPTG_REGION_CODE_NAMESPACE, value=region_code)
        ]

        self._add_names_from_elem(locality, elem)

        for district_elem in elem.findall(self._DISTRICT_XPATH):
            yield self._build_district(district_elem, locality)

        yield locality

    def _build_district(self, elem, region):
        locality = self._build_base_locality(elem)
        district_code = elem.find(self._DISTRICT_CODE_XPATH).text

        locality.url = region.url + "/" + district_code
        locality.parent_url = region.url
        locality.identifiers = [
            Identifier(namespace=NPTG_DISTRICT_CODE_NAMESPACE, value=district_code)
        ]

        self._add_names_from_elem(locality, elem)

        return locality

    def _add_names_from_elem(self, locality, elem):
        for name_elem in elem.findall(self._REGION_DISTRICT_NAME_XPATH):
            locality.identifiers.add(
                Identifier(namespace="human", value=name_elem.text, lang=name_elem.attrib.get(self._LANGUAGE_ATTRIB))
            )

    def _build_locality(self, elem):
        locality = self._build_base_locality(elem)
        locality_code = elem.find(self._LOCALITY_CODE_XPATH).text

        locality.url = "/" + locality_code

        locality.identifiers = [
            Identifier(namespace=NPTG_LOCALITY_CODE_NAMESPACE, value=locality_code)
        ]

        return locality
