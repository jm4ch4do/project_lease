from django.core.exceptions import ValidationError


def at_least_one_required(fields, noun):
    """ At least one of the fields must have a value """

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



def exclusive_fields(fields, noun):
    """ If one field has a value the other can't have a value """

    # count of values in fields can't be higher than one
    count = 0
    for value in fields:
        if value:
            count += 1

        if count > 1:
            raise ValidationError(
                "You can have only one of this values set %(noun)s",
                code='exclusive_fields',
                params={'noun': noun}
            )

    return fields\



def higher_eq_than(value, minimum, noun):
    """ value should be higher or equal than limit """

    if value < minimum:
        raise ValidationError(
            "The value %(noun) should be higher than %(minimum)",
            code='higher_eq_than',
            params={'noun': noun}
        )


def repeated_values(values, noun):
    """ values can't have repeated (duplicated) objects """

    if len(set(values)) != len(values):
        raise ValidationError(
            "You can't have repeated values in %(noun)",
            code='repeated_values',
            params={'noun': noun}
        )
