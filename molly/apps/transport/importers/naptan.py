import xml.etree.cElementTree as ElementTree

from django.contrib.gis.geos import Point

from tch.common.models import Identifier
from tch.importers.common import ZippedUrlImporter, Parser
from tch.stops.models import CallingPoint, Locality, Stop, Type

class NaptanImporter(ZippedUrlImporter):
    
    HTTP_HOST = "www.dft.gov.uk"
    REMOTE_PATH = "/NaPTAN/snapshot/NaPTANxml.zip"
    
    def do_import(self):
        naptan_parser = NaptanParser(self._url, self._get_naptan())
        naptan_parser.import_stops()
        
        self._http_connection.close()
    
    def _get_naptan(self):
        return self._get_zipped_from_url(self.REMOTE_PATH).open('NaPTAN.xml')


class NaptanParser(Parser):
    
    ATCO_CODE_NAMESPACE = 'atco'
    NAPTAN_CODE_NAMESPACE = 'naptan'
    
    def __init__(self, source_url, file):
        self._file = file
        self._source_url = source_url
        self._stop_points = []
    
        self._STOP_POINT_HANDLERS = {
            'BCT': (self._process_bus_stop, 'bus-stop', 'Bus stop'),
            
            'AIR': (self._process_entrance, 'entrance', 'Entrance'),
            'GAT': (self._process_access_area, 'airport', 'Airport'),
            
            'FTD': (self._process_entrance, 'entrance', 'Entrance'),
            'FER': (self._process_access_area, 'ferry-terminal', 'Ferry terminal/port'),
            'FBT': (self._process_platform, 'ferry-berth', 'Ferry terminal/port berth'),
            
            'RSE': (self._process_entrance, 'entrance', 'Entrance'),
            'RLY': (self._process_access_area, 'rail-station', 'Rail station'),
            'RPL': (self._process_platform, 'platform', 'Platform'),
            
            'TMU': (self._process_entrance, 'entrance', 'Entrance'),
            'MET': (self._process_access_area, 'metro-station', 'Tram/metro/underground station'),
            'PLT': (self._process_platform, 'platform', 'Platform'),
            
            'LCE': (self._process_entrance, 'entrance', 'Entrance'),
            'LCB': (self._process_access_area, 'cable-car', 'Cable car'),
            'LPL': (self._process_platform, 'platform', 'Platform'),
            
            'BCE': (self._process_entrance, 'entrance', 'Entrance'),
            'BST': (self._process_access_area, 'bus-station', 'Bus station'),
            'BCS': (self._process_platform, 'bus-stop', 'Bus stop'),
            'BCQ': (self._process_platform, 'bus-stop', 'Bus stop'),
        }
    
    def import_stops(self):
        for event, elem in ElementTree.iterparse(self._file, events=('start', 'end',)):
            if elem.tag == '{http://www.naptan.org.uk/}NaPTAN' and event == 'start':
                self._source_file = elem.attrib['FileName']
                root_elem = elem
            
            if elem.tag == '{http://www.naptan.org.uk/}StopPoint' and event == 'end':
                self._process_stop_point(elem)
                root_elem.clear()
    
    def _process_stop_point(self, elem):
        stop_type = elem.find('./{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}StopType').text
        handler, type_slug, type_name = self._STOP_POINT_HANDLERS.get(stop_type, (None, None, None))
        if handler is not None:
            stop_type, created = Type.objects.get_or_create(slug=type_slug, type=type_name)
            handler(elem, stop_type)
    
    def _process_bus_stop(self, elem, stop_type):
        atco_code = elem.find('./{http://www.naptan.org.uk/}AtcoCode').text
        version = elem.attrib['RevisionNumber']
        
        try:
            stop = self._get_from_source_id(atco_code, Stop)
            stop_changed = self._get_this_source(stop).source_version != version
        except Stop.DoesNotExist:
            stop = Stop.objects.create(slug=atco_code, type=stop_type)
            self._create_source(stop, id, source_version)
            stop_changed = True
        
        if stop_changed:
            atco_id = self._update_identifier(stop, self.ATCO_CODE_NAMESPACE, atco_code)
                
            naptan_code = elem.find('./{http://www.naptan.org.uk/}NaptanCode').text
            naptan_id = self._update_identifier(stop, self.NAPTAN_CODE_NAMESPACE, naptan_code)
            human_name = self._determine_stop_name(self, elem)
            human_id = self._update_identifier(stop, "human", human_name)
            print human_name
            
            lat = elem.find('./{http://www.naptan.org.uk/}Place/{http://www.naptan.org.uk/}Location/{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Longitude')
            lon = elem.find('./{http://www.naptan.org.uk/}Place/{http://www.naptan.org.uk/}Location/{http://www.naptan.org.uk/}Translation/{http://www.naptan.org.uk/}Latitude')
            
            location = Point(float(lat.text), float(lon.text), srid=4326)
            
            admin_ref = elem.find('./{http://www.naptan.org.uk/}AdministrativeAreaRef').text
            admin_org = Organisation.objects.get_by_id('nptg/AdministrativeAreaCode', admin_ref)
            
            stop.administrator = admin_org
            stop.location = location
            
            stop.primary_locality = Locality.objects.get_by_id(
                'nptg/LocalityCode',
                elem.find('./{http://www.naptan.org.uk/}Place/{http://www.naptan.org.uk/}NptgLocalityRef').text
            )
            stop.localities.clear()
            stop.localities.add(Locality.objects.get_by_id('nptg/LocalityCode', e.text)
                                for e in elem.findall('{http://www.naptan.org.uk/}NptgLocalityRef'))
            stop.save()
            
            try:
                calling_point = CallingPoint.objects.get_from_source(
                    self._get_this_source(stop)
                )
            except CallingPoint.DoesNotExist:
                calling_point = CallingPoint.objects.create(slug=slug, type=stop_type)
                calling_point.sources.add(self._get_this_source(stop))
                calling_point.identifiers.add(atco_id, naptan_id, human_id)
            calling_point.location = location
            calling_point.save()
            
            self._update_source_version(stop, version)
    
    def _determine_stop_name(self, elem):
        return elem.find('./{http://www.naptan.org.uk/}Descriptor/{http://www.naptan.org.uk/}CommonName').text
    
    def _process_access_area(self, elem, stop_type):
        pass
    
    def _process_entrance(self, elem, stop_type):
        pass
    
    def _process_platform(self, elem, stop_type):
        pass
