from datetime import date


def age_from_dob(dob):
    """" Calculates age using date of birth (dob) """

    # find years_passed since dob
    today = date.today()
    diff_in_years = today.year - dob.year

    # find if birthday already passed the current year
    if today.month < dob.month:
        has_birthday_passed = False
    elif today.month > dob.month:
        has_birthday_passed = True
    elif today.day >= dob.day:
        has_birthday_passed = True
    else:
        has_birthday_passed = False

    # decide if age is years_passed or years_passed+1
    age = diff_in_years if has_birthday_passed else diff_in_years - 1

    return age
