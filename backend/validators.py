import re


def validate_password(password):
    """
    Verify the strength of 'password'
    Returns 'None' if some of rules failed, otherwise 'True'
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    if any([digit_error, length_error, uppercase_error, lowercase_error, symbol_error]):
        return None

    return True
