from tch.stop import CallingPoint, Stop

class StopMongoDb(object):

    def __init__(self, connection):
        self._connection = connection
        self._connection.ensure_index('url')
        self._connection.ensure_index('identifiers')

    def _query_by_url(self, url, filter_by_type):
        query = {'url': url}
        if filter_by_type:
            query['_type'] = filter_by_type
        return self._connection.find_one(query)

    def select_by_url(self, url, filter_by_type=None):
        return self._parse_response(self._query_by_url(url, filter_by_type=self._get_type(filter_by_type)))

    def select_by_identifier(self, *identifiers, **kwargs):
        filter_by_type = kwargs.get('filter_by_type')
        query = [{'identifiers': [identifier._asdict()]} for identifier in identifiers]
        if filter_by_type:
            for query_part in query:
                query_part['_type'] = self._get_type(filter_by_type)
        return map(lambda found: self._parse_response(found), self._connection.find({'$or': query}))

    def insert(self, stop):
        stop_dict = stop._asdict()
        existing_stop_dict = self._query_by_url(stop.url)
        if existing_stop_dict is not None:
            stop_dict['_id'] = existing_stop_dict['_id']
        stop_dict['_type'] = self._get_type(type(stop))
        self._connection.save(stop_dict)

    def _parse_response(self, stop_dict):
        if stop_dict is None:
            return None
        elif stop_dict.get('_type') == 'stop':
            return Stop.from_dict(stop_dict)
        elif stop_dict.get('_type') == 'calling-point':
            return CallingPoint.from_dict(stop_dict)

    def _get_type(self, stop_type):
        if stop_type is Stop:
            return 'stop'
        elif stop_type is CallingPoint:
            return 'calling-point'
