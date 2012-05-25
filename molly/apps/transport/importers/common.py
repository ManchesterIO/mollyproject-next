import httplib
import tempfile
from zipfile import ZipFile

from django.core.exceptions import ObjectDoesNotExist

class ZippedUrlImporter():
    
    def __init__(self, http_connection=None):
        self._http_connection = http_connection
        if http_connection is None:
            self._http_connection = httplib.HTTPConnection(self.HTTP_HOST)
        else:
            self._http_connection = http_connection
        
        self._url = "http://%s%s" % (self.HTTP_HOST, self.REMOTE_PATH)
    
    def _get_zipped_from_url(self, url):
        temporary = tempfile.TemporaryFile()
        self._http_connection.request('GET', url)
        temporary.write(self._http_connection.getresponse().read())
        return ZipFile(temporary)


class Parser():
    
    def _get_from_source_id(self, id, model):
        return model.objects.get_by_source_id(self._source_url, self._source_file, id)
    
    def _get_this_source(self, obj):
        return obj.sources.get(source_url=self._source_url, source_file=self._source_file)
    
    def _create_source(self, obj, id, version):
        obj.sources.create(
            source_url=self._source_url,
            source_file=self._source_file,
            source_id=id,
            source_version=version
        )
    
    def _update_identifier(self, obj, namespace, elem):
        try:
            identifier = obj.identifiers.get(namespace=namespace,
                language=elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'))
            identifier.value = elem.text
            identifier.save()
        except ObjectDoesNotExist:
            identifier = obj.identifiers.create(
                namespace=namespace,
                value=elem.text,
                language=elem.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            )
        return identifier
    
    def _update_source_version(self, obj, version):
        source = self._get_this_source(obj)
        source.source_version = version
        source.save()
