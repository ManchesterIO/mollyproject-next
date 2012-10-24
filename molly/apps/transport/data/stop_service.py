from tch.data.base import BaseService

class StopService(BaseService):

    def __init__(self, connection):
        self._connection = connection

    def insert_and_merge(self, stop):
        existing_stop = self._connection.select_by_url(stop.url)
        if existing_stop is None or self._update_needed(existing_stop, stop):
            # TODO: Merge existing with new
            self._connection.insert(stop)
