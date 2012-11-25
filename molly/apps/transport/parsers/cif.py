from tch.identifier import Identifier
from tch.source import Source
from tch.stop import CallingPoint, TIPLOC_NAMESPACE, STANOX_NAMESPACE, CRS_NAMESPACE, CIF_DESCRIPTION_NAMESPACE

class CifParser(object):

    _SOURCE_URL = 'cif:'
    _LICENCE = 'Creative Commons Attribution-ShareAlike'
    _LICENCE_URL = 'http://creativecommons.org/licenses/by-sa/1.0/legalcode'
    _ATTRIBUTION = '<a href="http://www.atoc.org/">Source: RSP</a>'

    def import_from_file(self, archive):
        self.tiplocs = []
        self._parse_mca_file(archive)

    def _parse_mca_file(self, archive):
        handlers = {
            'TI': self._handle_tiploc_insert
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
        tiploc = CallingPoint()
        tiploc.sources.add(self._source)
        tiploc.identifiers.add(Identifier(namespace=TIPLOC_NAMESPACE, value=line[2:9].strip()))
        tiploc.identifiers.add(Identifier(namespace=CIF_DESCRIPTION_NAMESPACE, value=line[18:44].strip().title()))
        tiploc.identifiers.add(Identifier(namespace=STANOX_NAMESPACE, value=line[44:49]))
        crs_code = line[53:56].strip()
        if crs_code:
            tiploc.identifiers.add(Identifier(namespace=CRS_NAMESPACE, value=line[53:56]))
        self.tiplocs.append(tiploc)

