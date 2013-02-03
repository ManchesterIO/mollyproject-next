from molly.apps.transport.data.base import BaseService

class LocalityService(BaseService):

    def __init__(self, connection):
        self._connection = connection

    def locality_by_url(self, locality_url):
        return self._connection.select_by_url(locality_url)

    def insert_and_merge(self, locality):
        existing_locality = self.locality_by_url(locality.url)

        if existing_locality is None:
            self._connection.insert(locality)
        elif self._update_needed(existing_locality, locality):
            self._connection.insert(self._merge_localities(existing_locality, locality))

    def _merge_localities(self, existing_locality, locality):
        self._merge_attribute('parent_url', existing_locality, locality)
        self._merge_attribute('geography', existing_locality, locality)
        existing_locality.identifiers.update(locality.identifiers)
        existing_locality.sources.update(locality.sources)
        return existing_locality
