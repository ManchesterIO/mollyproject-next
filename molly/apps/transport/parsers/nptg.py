from xml.etree.cElementTree import iterparse

from shapely.geometry.point import Point
from molly.apps.common.components import Source, Identifier, Identifiers, Attribution, LocalisedName
from molly.apps.transport.models import Locality, NPTG_REGION_CODE_NAMESPACE, NPTG_DISTRICT_CODE_NAMESPACE, NPTG_LOCALITY_CODE_NAMESPACE

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
    _LOCALITY_NAME_XPATH = './{http://www.naptan.org.uk/}Descriptor/{http://www.naptan.org.uk/}LocalityName'
    _LOCALITY_LATITUDE_XPATH = './{http://www.naptan.org.uk/}Location/{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Latitude'
    _LOCALITY_LONGITUDE_XPATH = './{http://www.naptan.org.uk/}Location/{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Longitude'
    _LOCALITY_DISTRICT_REF_XPATH = './{http://www.naptan.org.uk/}NptgDistrictRef'
    _LOCALITY_PARENT_REF_XPATH = './{http://www.naptan.org.uk/}ParentNptgLocalityRef'

    _ATTRIBUTION = Attribution(
        attribution_text="Contains public sector information licensed under the Open Government Licence v1.0",
        licence_name='Open Government Licence',
        licence_url='http://www.nationalarchives.gov.uk/doc/open-government-licence/'
    )

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
            Source(
                url=self._source_url + "/" + self._source_file,
                version=elem.attrib['RevisionNumber'],
                attribution=self._ATTRIBUTION
            )
        ]
        return locality

    def _build_region(self, elem):
        locality = self._build_base_locality(elem)
        region_code = elem.find(self._REGION_CODE_XPATH).text

        locality.url = "/gb/" + region_code
        locality.identifiers = Identifiers([
            Identifier(namespace=NPTG_REGION_CODE_NAMESPACE, value=region_code)
        ])

        self._add_names_from_elem(locality, elem)

        for district_elem in elem.findall(self._DISTRICT_XPATH):
            yield self._build_district(district_elem, locality)

        yield locality

    def _build_district(self, elem, region):
        locality = self._build_base_locality(elem)
        district_code = elem.find(self._DISTRICT_CODE_XPATH).text

        locality.url = "/gb/" + district_code
        locality.parent_url = region.url
        locality.identifiers = [
            Identifier(namespace=NPTG_DISTRICT_CODE_NAMESPACE, value=district_code)
        ]

        self._add_names_from_elem(locality, elem)

        return locality

    def _add_names_from_elem(self, locality, elem):
        for name_elem in elem.findall(self._REGION_DISTRICT_NAME_XPATH):
            locality.names.add(self._build_name_from_elem(name_elem))

    def _build_locality(self, elem):
        locality = self._build_base_locality(elem)

        locality_code = elem.find(self._LOCALITY_CODE_XPATH).text
        name_elem = elem.find(self._LOCALITY_NAME_XPATH)
        lat = elem.find(self._LOCALITY_LATITUDE_XPATH).text
        lon = elem.find(self._LOCALITY_LONGITUDE_XPATH).text
        parent_elem = elem.find(self._LOCALITY_PARENT_REF_XPATH)

        if parent_elem is None:
            district_ref = elem.find(self._LOCALITY_DISTRICT_REF_XPATH).text
            locality.parent_url = '/gb/' + district_ref
        else:
            locality.parent_url = '/gb/' + parent_elem.text

        locality.url = "/gb/" + locality_code

        locality.identifiers = Identifiers([
            Identifier(namespace=NPTG_LOCALITY_CODE_NAMESPACE, value=locality_code)
        ])
        locality.names.add(self._build_name_from_elem(name_elem))

        locality.geography = Point(float(lon), float(lat))

        return locality

    def _build_name_from_elem(self, elem):
        lang = elem.attrib.get(self._LANGUAGE_ATTRIB)
        if lang is not None:
            lang = lang.lower()

        return LocalisedName(name=elem.text, lang=lang)
