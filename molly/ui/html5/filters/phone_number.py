import phonenumbers

from molly.ui.html5.filters import register_filter

@register_filter('format_telephone_number')
def format_telephone_number(telephone_number, **kwargs):
    try:
        return phonenumbers.format_number(
            phonenumbers.parse(telephone_number), phonenumbers.PhoneNumberFormat.NATIONAL
        )
    except phonenumbers.NumberParseException:
        return telephone_number
