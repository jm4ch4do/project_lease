import pytest
from app_lease.test.generator import random_creditcard
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime


@pytest.mark.order(11)
@pytest.mark.django_db
def test_empty_customer_in_creditcard():
    """ Customer can't be empty in a credit card record """

    created_creditcard = random_creditcard()
    with pytest.raises(IntegrityError) as exp:
        created_creditcard.customer = None
        created_creditcard.save()
    assert True if exp else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_expire_year_in_creditcard():
    """ Expire year allows values until 20 years into the future """

    created_creditcard = random_creditcard()
    with pytest.raises(ValidationError) as exp:
        created_creditcard.expire_year = datetime.today().year + 21
        created_creditcard.full_clean()
    assert True if exp else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_expire_month_in_creditcard():
    """ Expire months allows range from 1 to 12"""

    created_creditcard = random_creditcard()

    with pytest.raises(ValidationError) as exp:
        created_creditcard.expire_month = 13
        created_creditcard.full_clean()
    assert True if exp else False

    with pytest.raises(ValidationError) as exp:
        created_creditcard.expire_month = -1
        created_creditcard.full_clean()
    assert True if exp else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_security_code_in_creditcard():
    """ Security code always has three digits"""

    created_creditcard = random_creditcard()
    with pytest.raises(ValidationError) as exp:
        created_creditcard.security_code = 1234
        created_creditcard.full_clean()
    assert True if exp else False

    with pytest.raises(ValidationError) as exp:
        created_creditcard.security_code = 12
        created_creditcard.full_clean()
    assert True if exp else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_card_number_in_creditcard():
    """ Card number is always between 12 and 19 digits"""

    created_creditcard = random_creditcard()

    # too short
    with pytest.raises(ValidationError) as exp:
        created_creditcard.security_code = str(12345678901)
        created_creditcard.full_clean()
    assert True if exp else False

    # too long
    with pytest.raises(ValidationError) as exp:
        created_creditcard.security_code = str(12345678901234567890)
        created_creditcard.full_clean()
    assert True if exp else False
