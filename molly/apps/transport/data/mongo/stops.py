from tch.stop import CallingPoint, Stop

class StopMongoDb(object):

    def __init__(self, connection):
        self._connection = connection
        self._connection.ensure_index('url')

    def _query_by_url(self, url):
        return self._connection.find_one({'url': url})

    def select_by_url(self, url):
        stop_dict = self._query_by_url(url)
        if stop_dict is None:
            return None
        elif stop_dict.get('_type') == 'stop':
            return Stop.from_dict(stop_dict)
        elif stop_dict.get('_type') == 'calling-point':
            return CallingPoint.from_dict(stop_dict)

    def insert(self, stop):
        stop_dict = stop.as_dict()
        existing_stop_dict = self._query_by_url(stop.url)
        if existing_stop_dict is not None:
            stop_dict['_id'] = existing_stop_dict['_id']
        if isinstance(stop, Stop):
            stop_dict['_type'] = 'stop'
        elif isinstance(stop, CallingPoint):
            stop_dict['_type'] = 'calling-point'
        self._connection.save(stop_dict)
