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
