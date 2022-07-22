from django.core.exceptions import ValidationError


# at_least one of the fields must have a value
def at_least_one_required(fields, noun):

    # if at least a field has a value -> OK
    for value in fields:
        if value:
            break

    # but if no field has value -> Raise Error
    else:
        raise ValidationError(
            'Please provide at least one %(noun)s',
            code='at_least_one',
            params={'noun': noun}
        )

    return fields\
