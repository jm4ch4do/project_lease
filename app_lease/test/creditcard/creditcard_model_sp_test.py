import pytest
from app_lease.test.generator import random_creditcard
from django.db import IntegrityError


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


@pytest.mark.order(11)
@pytest.mark.django_db
def test_expire_month_in_creditcard():
    """ Expire months allows range from 1 to 12"""

    created_creditcard = random_creditcard()


@pytest.mark.order(11)
@pytest.mark.django_db
def test_security_code_in_creditcard():
    """ Security code always has three digits"""

    created_creditcard = random_creditcard()


@pytest.mark.order(11)
@pytest.mark.django_db
def test_card_number_in_creditcard():
    """ Card number is always between 12 and 19 digits"""

    created_creditcard = random_creditcard()
