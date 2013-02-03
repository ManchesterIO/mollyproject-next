from tch.locality import Locality

class LocalityMongoDb(object):

    def __init__(self, collection):
        self._collection = collection
        self._collection.ensure_index('url')

    def _query_by_url(self, url):
        return self._collection.find_one({'url': url})

    def select_by_url(self, url):
        locality_dict = self._query_by_url(url)
        if locality_dict is None:
            return None
        else:
            return Locality.from_dict(locality_dict)

    def insert(self, locality):
        locality_dict = locality.as_dict()
        existing_locality_dict = self._query_by_url(locality.url)
        if existing_locality_dict is not None:
            locality_dict['_id'] = existing_locality_dict['_id']
        self._collection.save(locality_dict)
