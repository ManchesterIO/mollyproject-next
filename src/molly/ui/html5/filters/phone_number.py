import phonenumbers


def format_telephone_number(telephone_number):
    try:
        return phonenumbers.format_number(
            phonenumbers.parse(telephone_number), phonenumbers.PhoneNumberFormat.NATIONAL
        )
    except phonenumbers.NumberParseException:
        return telephone_number
