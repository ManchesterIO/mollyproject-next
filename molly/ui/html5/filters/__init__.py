FILTERS = {}


def register_filter(filter_name):
    def decorator(fn):
        def filter_constructor(**global_kwargs):
            def wrapped_filter(*args, **kwargs):
                kwargs.update(global_kwargs)
                return fn(*args, **kwargs)
            return wrapped_filter
        FILTERS[filter_name] = filter_constructor
        return fn
    return decorator


def register_default_filters():
    import molly.ui.html5.filters.phone_number
    import molly.ui.html5.filters.render
