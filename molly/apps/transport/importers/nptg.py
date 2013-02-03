import httplib
from tempfile import TemporaryFile
from zipfile import ZipFile

from tch.parsers.nptg import NptgParser

class NptgImporter(object):

    HTTP_HOST = "www.dft.gov.uk"
    REMOTE_PATH = "/nptg/snapshot/nptgxml.zip"

    def __init__(self, locality_service):
        self._http_connection = httplib.HTTPConnection(self.HTTP_HOST)
        self._url = "http://%s%s" % (self.HTTP_HOST, self.REMOTE_PATH)
        self._locality_service = locality_service

    def _get_file_from_url(self):
        temporary = TemporaryFile()
        self._http_connection.request('GET', self._url)
        temporary.write(self._http_connection.getresponse().read())
        return ZipFile(temporary).open('NPTG.xml')

    def start(self):
        parser = NptgParser()
        for locality in parser.import_from_file(self._get_file_from_url(), self._url):
            self._locality_service.insert_and_merge(locality)
