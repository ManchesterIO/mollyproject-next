import xml.etree.cElementTree as ElementTree

from django.contrib.gis.geos import Point

from tch.common.models import Identifier
from tch.importers.common import ZippedUrlImporter, Parser
from tch.stops.models import Locality

class NptgImporter(ZippedUrlImporter):
    
    HTTP_HOST = "www.dft.gov.uk"
    REMOTE_PATH = "/nptg/snapshot/nptgxml.zip"
    
    def do_import(self):
        nptg_parser = NptgParser(self._url, self._get_nptg())
        nptg_parser.import_localities()
        
        self._http_connection.close()
    
    def _get_nptg(self):
        return self._get_zipped_from_url(self.REMOTE_PATH).open('NPTG.xml')


class NptgParser(Parser):
    
    _model = Locality
    
    REGION_CODE_NAMESPACE = 'nptg/RegionCode'
    ADMINISTRATIVE_AREA_CODE_NAMESPACE = 'nptg/AdministrativeAreaCode'
    ATCO_AREA_CODE_NAMESPACE = 'nptg/AtcoAreaCode'
    LOCALITY_CODE_NAMESPACE = 'nptg/LocalityCode'
    NAPTAN_PREFIX_NAMESPACE = 'nptg/NaptanPrefix'
    
    def __init__(self, source_url, file):
        self._file = file
        self._source_url = source_url
        self._source_file = None
        self._localities = {}
        self._unset_parents = []
    
    def import_localities(self):
        for event, elem in ElementTree.iterparse(self._file, events=('start', 'end',)):
            
            if elem.tag == '{http://www.naptan.org.uk/}NationalPublicTransportGazetteer' and event == 'start':
                self._source_file = elem.attrib['FileName']
            
            if elem.tag == '{http://www.naptan.org.uk/}Region' and event == 'end':
                self._process_region(elem)
                elem.clear()
            
            if elem.tag == '{http://www.naptan.org.uk/}NptgLocality' and event == 'end':
                self._process_locality(elem)
                elem.clear()
            
            if elem.tag == '{http://www.naptan.org.uk/}NptgLocalities' and event == 'end':
                for locality in self._unset_parents:
                    locality.parent = self._localities[locality.parent_]
                    locality.save()
                elem.clear()
    
    
    def _process_region(self, elem):
        region_code = elem.find('{http://www.naptan.org.uk/}RegionCode').text
        version = elem.attrib['RevisionNumber']
        
        region, region_version_changed = self._fetch_locality(
            region_code,
            self.REGION_CODE_NAMESPACE,
            'nptg/' + region_code,
            version
        )
        
        if region_version_changed:
            for name_elem in elem.findall('./{http://www.naptan.org.uk/}Name'):
                self._update_identifier(region, "human", name_elem)
            
            self._update_source_version(region, version)
        
        for administrative_area_elem in elem.findall(
            './{http://www.naptan.org.uk/}AdministrativeAreas/{http://www.naptan.org.uk/}AdministrativeArea'
        ):
            self._process_administrative_area(administrative_area_elem, region)
    
    def _process_administrative_area(self, elem, parent):
        area_code = elem.find('{http://www.naptan.org.uk/}AdministrativeAreaCode').text
        version = elem.attrib['RevisionNumber']
        
        try:
            area = self._get_from_source_id(area_code, Organisation)
        except Organisation.DoesNotExist:
            area = Organisation.objects.create(slug=slug, type='administrator')
            self._create_source(area, id, source_version)
            area.identifiers.create(
                namespace=self.ADMINISTRATIVE_AREA_CODE_NAMESPACE,
                value=area_code
            )
        
        if self._get_this_source(area).source_version != version:
            self._update_identifier(
                area,
                self.ATCO_AREA_CODE_NAMESPACE,
                elem.find('./{http://www.naptan.org.uk/}AtcoAreaCode')
            )
            
            for name_elem in elem.findall('./{http://www.naptan.org.uk/}Name'):
                self._update_identifier(area, "human", name_elem)
                
            for short_name_elem in elem.findall('./{http://www.naptan.org.uk/}ShortName'):
                self._update_identifier(area, "human_short", short_name_elem)
                
            area.identifiers.filter(namespace=self.NAPTAN_PREFIX_NAMESPACE).delete()
            for prefix_elem in elem.findall('./{http://www.naptan.org.uk/}NaptanPrefixes/{http://www.naptan.org.uk/}AlphaPrefix'):
                area.identifiers.create(
                        namespace=self.NAPTAN_PREFIX_NAMESPACE,
                        value=prefix_elem.text
                    )
            
            self._update_source_version(area, version)
        
        for district_elem in elem.findall('./{http://www.naptan.org.uk/}NptgDistricts/{http://www.naptan.org.uk/}NptgDistrict'):
            self._process_district(district_elem, parent)
    
    def _process_district(self, elem, parent):
        district_code = elem.find('{http://www.naptan.org.uk/}NptgDistrictCode').text
        version = elem.attrib['RevisionNumber']
        
        district, district_version_changed = self._fetch_locality(
            district_code,
            self.REGION_CODE_NAMESPACE,
            parent.slug + '/' + district_code,
            version
        )
        
        self._localities[district_code] = district
        
        if district_version_changed:
            district.parent = parent
            district.save()
            
            for name_elem in elem.findall('./{http://www.naptan.org.uk/}Name'):
                self._update_identifier(district, "human", name_elem)
            
            self._update_source_version(district, version)
    
    def _process_locality(self, elem):
        locality_code = elem.find('{http://www.naptan.org.uk/}NptgLocalityCode').text
        version = elem.attrib['RevisionNumber']
        
        locality, locality_version_changed = self._fetch_locality(
            locality_code,
            self.LOCALITY_CODE_NAMESPACE,
            'nptg/' + locality_code,
            version
        )
        
        self._localities[locality_code] = locality
        
        if locality_version_changed:
            
            locality.identifiers.filter(namespace="human").delete()
            for descriptor_elem in elem.findall('.//{http://www.naptan.org.uk/}Descriptor'):
                self._process_descriptor(locality, descriptor_elem)
            
            parent_elem = elem.find('./{http://www.naptan.org.uk/}ParentNptgLocalityRef')
            if parent_elem is None:
                parent_elem = elem.find('./{http://www.naptan.org.uk/}NptgDistrictRef')
            
            lat = elem.find('./{http://www.naptan.org.uk/}Location/{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Longitude')
            lon = elem.find('./{http://www.naptan.org.uk/}Location/{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Latitude')
            
            locality.centre = Point(float(lat.text), float(lon.text), srid=4326)
            
            if parent_elem.text not in self._localities:
                locality.parent_ = parent_elem.text
            else:
                locality.parent = self._localities[parent_elem.text]
                locality.save()
            
            self._update_source_version(locality, version)
    
    def _process_descriptor(self, locality, elem):
        name = elem.find('./{http://www.naptan.org.uk/}LocalityName')
        qualifier = elem.find('./{http://www.naptan.org.uk/}Qualify/{http://www.naptan.org.uk/}QualifyName')
        
        if qualifier is None or qualifier.attrib.get('{http://www.w3.org/XML/1998/namespace}lang') \
            != name.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'):
            locality_name = name.text
        else:
            locality_name = "%s (%s)" % (name.text, qualifier.text)
        
        locality.identifiers.create(namespace="human", value=locality_name,
            language=elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'))
    
    def _fetch_locality(self, id, namespace, slug, source_version):
        try:
            locality = self._get_from_source_id(id, Locality)
            return locality, source_version == self._get_this_source(locality).source_version
        except Locality.DoesNotExist:
            locality = Locality.objects.create(slug=slug)
            self._create_source(locality, id, source_version)
            locality.identifiers.create(
                namespace=namespace,
                value=id
            )
            return locality, True
