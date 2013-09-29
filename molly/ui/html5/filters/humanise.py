from flask.ext.babel import gettext as _


def humanise_distance(metres):
    if metres > 900:
        return _('%(distance).1f miles', distance=metres / 1609.344)
    else:
        return _('%(distance)dm', distance=metres)