from molly.apps.transport.models import Stop, CallingPoint, Locality

class BaseService(object):

    def _update_needed(self, existing, new):
        for existing_source in set(existing.sources):
            for new_source in new.sources:
                if existing_source == new_source:
                    return False
                elif existing_source.url == new_source.url:
                    existing.sources.remove(existing_source)
        return True

    def _merge_attribute(self, attribute, existing_locality, locality):
        if hasattr(locality, attribute):
            setattr(existing_locality, attribute, getattr(locality, attribute))


class LocalityService(BaseService):

    def __init__(self, connection):
        self._connection = connection
        self._connection.ensure_index('url')

    def locality_by_url(self, locality_url):
        return self._dict_to_locality(self._query_by_url(locality_url))

    def insert_and_merge(self, locality):
        existing_locality_dict = self._query_by_url(locality.url)

        if existing_locality_dict is None:
            self._insert(locality, existing_locality_dict)
        else:
            existing_locality = self._dict_to_locality(existing_locality_dict)
            if self._update_needed(existing_locality, locality):
                self._insert(self._merge_localities(existing_locality, locality), existing_locality_dict)

    def _merge_localities(self, existing_locality, locality):
        self._merge_attribute('parent_url', existing_locality, locality)
        self._merge_attribute('geography', existing_locality, locality)
        existing_locality.identifiers.update(locality.identifiers)
        existing_locality.sources.update(locality.sources)
        return existing_locality
    
    def _query_by_url(self, url):
        return self._connection.find_one({'url': url})

    def _dict_to_locality(self, locality_dict):
        if locality_dict is None:
            return None
        else:
            return Locality.from_dict(locality_dict)

    def _insert(self, locality, existing_locality_dict):
        locality_dict = locality._asdict()
        if existing_locality_dict is not None:
            locality_dict['_id'] = existing_locality_dict['_id']
        self._connection.save(locality_dict)


class StopService(BaseService):

    def __init__(self, connection):
        self._connection = connection
        self._connection.ensure_index('url')
        self._connection.ensure_index('identifiers')

    def select_by_url(self, url, filter_by_type=None):
        return self._parse_response(self._query_by_url(url, filter_by_type=self._get_type(filter_by_type)))

    def select_by_identifiers(self, *identifiers, **kwargs):
        filter_by_type = kwargs.get('filter_by_type')
        query = [{'identifiers': [identifier._asdict()]} for identifier in identifiers]
        if filter_by_type:
            for query_part in query:
                query_part['_type'] = self._get_type(filter_by_type)
        return map(lambda found: self._parse_response(found), self._connection.find({'$or': query}))

    def insert_and_merge(self, stop):
        """
        When the passed in Stop has an URL, it is merged with anything already existing that has that URL
        If the passed in stop does not have a URL (for example, some railway data sets refer to things
        only by STANOX, etc) then it is merged with things that share its identifiers
        """
        if stop.url is not None:
            self._do_insert_and_merge(self.select_by_url(stop.url, filter_by_type=type(stop)), stop)
        else:
            existing_stops = self.select_by_identifiers(*stop.identifiers, filter_by_type=type(stop))
            if len(existing_stops) == 0:
                self._do_insert_and_merge(None, stop)
            else:
                for existing_stop in existing_stops:
                    self._do_insert_and_merge(existing_stop, stop)

    def _do_insert_and_merge(self, existing_stop, stop):
        if existing_stop is None or self._update_needed(existing_stop, stop):
            if existing_stop is not None:
                stop = self._merge_stop(existing_stop, stop)
            stop_dict = stop._asdict()
            existing_stop_dict = self._query_by_url(stop.url)
            if existing_stop_dict is not None:
                stop_dict['_id'] = existing_stop_dict['_id']
            stop_dict['_type'] = self._get_type(type(stop))
            self._connection.save(stop_dict)

    def _merge_stop(self, existing_stop, stop):
        existing_stop.sources.update(stop.sources)
        existing_stop.identifiers.update(stop.identifiers)
        if isinstance(existing_stop, Stop):
            existing_stop.calling_points.update(stop.calling_points)
        elif isinstance(existing_stop, CallingPoint) and stop.url is not None:
            # Only change parent_url if our new model is fully formed, i.e., has a URL
            existing_stop.parent_url = stop.parent_url
        return existing_stop

    def _query_by_url(self, url, filter_by_type=None):
        query = {'url': url}
        if filter_by_type:
            query['_type'] = filter_by_type
        return self._connection.find_one(query)

    def _get_type(self, stop_type):
        if stop_type is Stop:
            return 'stop'
        elif stop_type is CallingPoint:
            return 'calling-point'

    def _parse_response(self, stop_dict):
        if stop_dict is None:
            return None
        elif stop_dict.get('_type') == 'stop':
            return Stop.from_dict(stop_dict)
        elif stop_dict.get('_type') == 'calling-point':
            return CallingPoint.from_dict(stop_dict)