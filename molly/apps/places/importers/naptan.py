from datetime import timedelta
import httplib
from tempfile import TemporaryFile
from zipfile import ZipFile
from celery.schedules import schedule

from molly.apps.places.parsers.naptan import NaptanParser


class NaptanImporter(object):

    IMPORTER_NAME = 'naptan'
    IMPORT_SCHEDULE = schedule(run_every=timedelta(weeks=1))

    HTTP_HOST = "www.dft.gov.uk"
    REMOTE_PATH = "/NaPTAN/snapshot/NaPTANxml.zip"

    def __init__(self, config):
        self._http_connection = httplib.HTTPConnection(self.HTTP_HOST)
        self._url = "http://%s%s" % (self.HTTP_HOST, self.REMOTE_PATH)

    def _get_file_from_url(self):
        temporary = TemporaryFile()
        self._http_connection.request('GET', self._url)
        temporary.write(self._http_connection.getresponse().read())
        return ZipFile(temporary).open('NaPTAN.xml')

    def load(self):
        parser = NaptanParser()
        for stop in parser.import_from_file(self._get_file_from_url(), self._url):
            self.poi_service.add_or_update(stop)


Provider = NaptanImporter
