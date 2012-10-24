import httplib
from tempfile import TemporaryFile
from zipfile import ZipFile
from tch.parsers.naptan import NaptanParser

class NaptanImporter(object):

    HTTP_HOST = "www.dft.gov.uk"
    REMOTE_PATH = "/NaPTAN/snapshot/NaPTANxml.zip"

    def __init__(self, stop_service):
        self._http_connection = httplib.HTTPConnection(self.HTTP_HOST)
        self._url = "http://%s%s" % (self.HTTP_HOST, self.REMOTE_PATH)
        self._stop_service = stop_service

    def _get_file_from_url(self):
        temporary = TemporaryFile()
        self._http_connection.request('GET', self._url)
        temporary.write(self._http_connection.getresponse().read())
        return ZipFile(temporary).open('NaPTAN.xml')

    def start(self):
        parser = NaptanParser()
        for stop in parser.import_from_file(self._get_file_from_url(), self._url):
            self._stop_service.insert_and_merge(stop)
