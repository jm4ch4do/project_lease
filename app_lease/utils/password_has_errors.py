import re


def password_has_errors(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    errors = []

    # calculating the length
    length_error = len(password) < 8
    if length_error:
        errors.append('length must be at least 8 characters')

    # searching for digits
    digit_error = re.search(r"\d", password) is None
    if digit_error:
        errors.append('Password must include digits')

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None
    if uppercase_error:
        errors.append('Password must include uppercase')

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    if lowercase_error:
        errors.append('Password must include lowercase')

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None
    if symbol_error:
        errors.append('Password must include symbols')

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return errors
