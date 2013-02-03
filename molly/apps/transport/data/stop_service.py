from tch.data.base import BaseService
from tch.stop import Stop, CallingPoint

class StopService(BaseService):

    def __init__(self, connection):
        self._connection = connection

    def insert_and_merge(self, stop):
        """
        When the passed in Stop has an URL, it is merged with anything already existing that has that URL
        If the passed in stop does not have a URL (for example, some railway data sets refer to things
        only by STANOX, etc) then it is merged with things that share its identifiers
        """
        if stop.url is not None:
            self._do_insert_and_merge(self._connection.select_by_url(stop.url, filter_by_type=type(stop)), stop)
        else:
            existing_stops = self._connection.select_by_identifiers(*stop.identifiers, filter_by_type=type(stop))
            if len(existing_stops) == 0:
                self._do_insert_and_merge(None, stop)
            else:
                for existing_stop in existing_stops:
                    self._do_insert_and_merge(existing_stop, stop)

    def _do_insert_and_merge(self, existing_stop, stop):
        if existing_stop is None or self._update_needed(existing_stop, stop):
            if existing_stop is not None:
                stop = self._merge_stop(existing_stop, stop)
            self._connection.insert(stop)

    def _merge_stop(self, existing_stop, stop):
        existing_stop.sources.update(stop.sources)
        existing_stop.identifiers.update(stop.identifiers)
        if isinstance(existing_stop, Stop):
            existing_stop.calling_points.update(stop.calling_points)
        elif isinstance(existing_stop, CallingPoint) and stop.url is not None:
            # Only change parent_url if our new model is fully formed, i.e., has a URL
            existing_stop.parent_url = stop.parent_url
        return existing_stop
