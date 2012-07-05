class LocalityMongoDbService(object):

    def __init__(self, mongodb_connection):
        self._collection = mongodb_connection.localities

    def locality_by_url(self, locality):
        return self._collection.find_one({'url': locality.url})

    def insert_and_merge(self, locality):
        existing_locality = self.locality_by_url(locality)

        if existing_locality is None:
            self._collection.insert(locality)
        elif self._update_needed(existing_locality, locality):
            self._collection.insert(self._merge_localities(existing_locality, locality))

    def _update_needed(self, existing_locality, locality):
        for i, existing_locality_source in enumerate(existing_locality.sources):
            for new_locality_source in locality.sources:
                if existing_locality_source == new_locality_source:
                    return False
                elif existing_locality_source.url == new_locality_source.url:
                    del existing_locality.sources[i]
        return True

    def _merge_localities(self, existing_locality, locality):
        existing_locality.sources += locality.sources
        return existing_locality
