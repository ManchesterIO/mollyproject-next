from datetime import timedelta
import httplib
from tempfile import TemporaryFile
from zipfile import ZipFile
from celery.schedules import schedule

from molly.apps.transport.parsers.nptg import NptgParser

class NptgImporter(object):
    IMPORTER_NAME = 'nptg'
    IMPORT_SCHEDULE = schedule(run_every=timedelta(weeks=1))

    HTTP_HOST = "www.dft.gov.uk"
    REMOTE_PATH = "/nptg/snapshot/nptgxml.zip"

    def __init__(self, config):
        self._http_connection = httplib.HTTPConnection(self.HTTP_HOST)
        self._url = "http://%s%s" % (self.HTTP_HOST, self.REMOTE_PATH)

    def _get_file_from_url(self):
        temporary = TemporaryFile()
        self._http_connection.request('GET', self._url)
        temporary.write(self._http_connection.getresponse().read())
        return ZipFile(temporary).open('NPTG.xml')

    def load(self):
        parser = NptgParser()
        for locality in parser.import_from_file(self._get_file_from_url(), self._url):
            self.locality_service.insert_and_merge(locality)


Provider = NptgImporter
