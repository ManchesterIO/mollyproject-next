from tch.identifier import Identifier
from tch.source import Source
from tch.stop import CallingPoint, TIPLOC_NAMESPACE, STANOX_NAMESPACE, CRS_NAMESPACE, CIF_DESCRIPTION_NAMESPACE
from tch.timetable import Route, Service

class CifParser(object):

    _SOURCE_URL = 'cif:'
    _LICENCE = 'Creative Commons Attribution-ShareAlike'
    _LICENCE_URL = 'http://creativecommons.org/licenses/by-sa/1.0/legalcode'
    _ATTRIBUTION = '<a href="http://www.atoc.org/">Source: RSP</a>'

    def import_from_file(self, archive):
        self._tiploc_descriptions = {}
        self.tiplocs = []
        self.routes = []
        self.services = []
        self._services = {}
        self._parse_mca_file(archive)

    def _parse_mca_file(self, archive):
        handlers = {
            'TI': self._handle_tiploc_insert,
            'BS': self._handle_journey_schedule_start,
            'LO': self._handle_journey_origin,
            'LI': self._handle_journey_call,
            'LT': self._handle_journey_end,
            'ZZ': self._handle_file_end
        }

        self._source = Source(
            url=self._SOURCE_URL,
            version=archive.namelist[0].split('.')[0],
            licence=self._LICENCE,
            licence_url=self._LICENCE_URL,
            attribution=self._ATTRIBUTION
        )

        with self._open_mca_file(archive) as mca_file:
            for line in mca_file:
                handler = handlers.get(line[:2])
                if handler is not None:
                    handler(line)

    def _open_mca_file(self, archive):
        mca_filename = filter(lambda fn: fn.endswith('.MCA'), archive.namelist)[0]
        return archive.open(mca_filename)

    def _handle_tiploc_insert(self, line):
        calling_point = CallingPoint()
        calling_point.sources.add(self._source)

        tiploc = line[2:9].strip()
        calling_point.identifiers.add(Identifier(namespace=TIPLOC_NAMESPACE, value=tiploc))

        description = line[18:44].strip().title()
        calling_point.identifiers.add(Identifier(namespace=CIF_DESCRIPTION_NAMESPACE, value=description))

        calling_point.identifiers.add(Identifier(namespace=STANOX_NAMESPACE, value=line[44:49]))

        crs_code = line[53:56].strip()
        if crs_code:
            calling_point.identifiers.add(Identifier(namespace=CRS_NAMESPACE, value=line[53:56]))

        self._tiploc_descriptions[tiploc] = description
        self.tiplocs.append(calling_point)

    def _handle_journey_schedule_start(self, line):
        self._current_calling_tiplocs = []

    def _handle_journey_origin(self, line):
        self._current_calling_tiplocs.append(line[2:9].strip())

    def _handle_journey_call(self, line):
        self._current_calling_tiplocs.append(line[2:9].strip())

    def _handle_journey_end(self, line):
        self._current_calling_tiplocs.append(line[2:9].strip())
        route = Route()
        route.url = '/gb/rail/{origin}-{destination}'.format(
            origin=self._current_calling_tiplocs[0],
            destination=self._current_calling_tiplocs[-1]
        )
        route.headline = '{origin} to {destination}'.format(
            origin=self._tiploc_descriptions[self._current_calling_tiplocs[0]],
            destination=self._tiploc_descriptions[self._current_calling_tiplocs[-1]]
        )

        start_and_end = frozenset({self._current_calling_tiplocs[0], self._current_calling_tiplocs[-1]})
        service = self._services.get(start_and_end)
        if service is None:
            service = Service()
            service.url = route.url
            self.services.append(service)
            self._services[start_and_end] = service
        service.routes.add(route.url)
        route.service_url = service.url

        self.routes.append(route)

    def _handle_file_end(self, line):
        pass

