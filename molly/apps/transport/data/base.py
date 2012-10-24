class BaseService(object):

    def _update_needed(self, existing, new):
        for i, existing_source in enumerate(existing.sources):
            for new_source in new.sources:
                if existing_source == new_source:
                    return False
                elif existing_source.url == new_source.url:
                    del existing.sources[i]
        return True

    def _merge_attribute(self, attribute, existing_locality, locality):
        if hasattr(locality, attribute):
            setattr(existing_locality, attribute, getattr(locality, attribute))
