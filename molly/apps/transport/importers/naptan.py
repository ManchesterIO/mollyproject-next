import xml.etree.cElementTree as ElementTree
import httplib
import tempfile
from zipfile import ZipFile

from tch.common.models import Identifier
from tch.stops.models import Locality

class NaptanImporter():
    
    HTTP_HOST = "www.dft.gov.uk"
    NAPTAN_PATH = "/NaPTAN/snapshot/NaPTANxml.zip"
    NPTG_PATH = "/nptg/snapshot/nptgxml.zip"
    
    def __init__(self, http_connection=None):
        self._http_connection = http_connection
        if http_connection is None:
            self._http_connection = httplib.HTTPConnection(self.HTTP_HOST)
        else:
            self._http_connection = http_connection
        
        self._nptg_source = None
        self._naptan_source = None
        
        self._nptg = None
        self._naptan = None
        
        self._nptg_url = "http://%s%s" % (self.HTTP_HOST, self.NPTG_PATH)
        self._naptan_url = "http://%s%s" % (self.HTTP_HOST, self.NAPTAN_PATH)
    
    def do_import(self):
        nptg_parser = NptgParser(self._nptg_url, self._get_nptg())
        nptg_parser.import_localities()
        
        self._http_connection.close()
    
    def _get_naptan(self):
        return self._get_zipped_from_url(self.NAPTAN_PATH).open('NaPTAN.xml')
    
    def _get_nptg(self):
        return self._get_zipped_from_url(self.NPTG_PATH).open('NPTG.xml')
    
    def _get_zipped_from_url(self, url):
        temporary = tempfile.TemporaryFile()
        self._http_connection.request('GET', url)
        temporary.write(self._http_connection.getresponse().read())
        return ZipFile(temporary)


class NptgParser():
    
    def __init__(self, source_url, file):
        self._root = None
        self._file = file
        self._stack = []
        self._source_url = source_url
        self._source_file = None
    
    def import_localities(self):
        for event, elem in ElementTree.iterparse(self._file, events=('start', 'end',)):
            if event == 'start':
                if elem.tag == '{http://www.naptan.org.uk/}NationalPublicTransportGazetteer':
                    self._source_file = elem.attrib['FileName']
                else:
                    self._stack.append(elem.tag)
                
                if tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region'
                ):
                    current_region = None
                    current_region_version = elem.attrib['RevisionNumber']
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                ):
                    current_administrative_area = None
                    current_administrative_area_version = elem.attrib['RevisionNumber']
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}NptgDistricts',
                    '{http://www.naptan.org.uk/}NptgDistrict',
                ):
                    current_district = None
                    current_district_version = elem.attrib['RevisionNumber']
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}NaptanPrefixes'
                ) and administrative_area_changed:
                    current_administrative_area.identifiers.filter(namespace='nptg/NaptanPrefix').delete()
            
            else:
                
                if tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}RegionCode'
                ):
                    current_region, region_changed = self._fetch_locality(
                        elem.text, "nptg/RegionCode", 'nptg/' + elem.text, current_region_version
                    )
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}Name'
                ) and region_changed:
                    
                    self._update_identifier(current_region, 'human', elem)
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}AdministrativeAreaCode',
                ):
                    current_administrative_area, administrative_area_changed = \
                        self._fetch_locality(elem.text, "nptg/AdministrativeAreaCode",
                                             current_region.slug + '/' + elem.text,
                                             current_administrative_area_version)
                    
                    if administrative_area_changed:
                        current_administrative_area.parent = current_region
                        current_administrative_area.save()
                 
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}AtcoAreaCode',
                ) and administrative_area_changed:
                    
                    self._update_identifier(current_administrative_area, 'nptg/AtcoAreaCode', elem)
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}Name'
                ) and administrative_area_changed:
                    
                    self._update_identifier(current_administrative_area, 'human', elem)
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}ShortName'
                ) and administrative_area_changed:
                    
                    self._update_identifier(current_administrative_area, 'human_short', elem)
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}NaptanPrefixes',
                    '{http://www.naptan.org.uk/}AlphaPrefix',
                ) and administrative_area_changed:
                    
                    current_administrative_area.identifiers.create(
                        namespace='nptg/NaptanPrefix',
                        value=elem.text
                    )
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}NptgDistricts',
                    '{http://www.naptan.org.uk/}NptgDistrict',
                    '{http://www.naptan.org.uk/}NptgDistrictCode',
                ):
                    current_district, district_changed = \
                        self._fetch_locality(elem.text, "nptg/DistrictCode",
                                             current_administrative_area.slug + '/' + elem.text,
                                             current_administrative_area_version)
                    
                    if district_changed:
                        current_district.parent = current_administrative_area
                        current_district.save()
                
                elif tuple(self._stack) == (
                    '{http://www.naptan.org.uk/}Regions',
                    '{http://www.naptan.org.uk/}Region',
                    '{http://www.naptan.org.uk/}AdministrativeAreas',
                    '{http://www.naptan.org.uk/}AdministrativeArea',
                    '{http://www.naptan.org.uk/}NptgDistricts',
                    '{http://www.naptan.org.uk/}NptgDistrict',
                    '{http://www.naptan.org.uk/}Name'
                ) and district_changed:
                    
                    self._update_identifier(current_district, 'human', elem)
                
                if elem.tag != '{http://www.naptan.org.uk/}NationalPublicTransportGazetteer':
                    self._stack.pop()
    
    def _get_from_source_id(self, id):
        return Locality.objects.get_by_source_id(self._source_url, self._source_file, id)
    
    def _get_this_source(self, locality):
        return locality.sources.get(source_url=self._source_url, source_file=self._source_file)
    
    def _fetch_locality(self, id, namespace, slug, source_version):
        try:
            
            locality = self._get_from_source_id(id)
            return locality, source_version == self._get_this_source(locality).source_version
        
        except Locality.DoesNotExist:
            
            locality = Locality.objects.create(slug=slug)
            locality.sources.create(
                source_url=self._source_url,
                source_file=self._source_file,
                source_id=id,
                source_version=source_version
            )
            locality.save()
            locality.identifiers.create(
                namespace=namespace,
                value=id
            )
            return locality, True
    
    def _update_identifier(self, locality, namespace, elem):
        try:
            identifier = locality.identifiers.get(namespace=namespace,
                language=elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'))
            identifier.value = elem.text
            identifier.save()
        except Identifier.DoesNotExist:
            locality.identifiers.create(namespace=namespace, value=elem.text,
                language=elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'))
