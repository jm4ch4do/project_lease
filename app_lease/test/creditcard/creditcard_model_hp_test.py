import pytest
from app_lease.models import Customer, CreditCard
from app_lease.test.generator import random_creditcard
from django.contrib.auth.models import User
from datetime import datetime


@pytest.mark.order(11)
@pytest.mark.django_db
def test_create_creditcard():
    """ Creating creditcard also creates related customer and user """

    created_creditcard = random_creditcard()
    assert True if isinstance(created_creditcard, CreditCard) else False
    assert True if CreditCard.objects.all().count() == 1 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if User.objects.all().count() == 1 else False
    assert True if CreditCard.objects.first().customer.id == Customer.objects.first().id else False
    assert True if Customer.objects.first().user.id == User.objects.first().id else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_delete_creditcard():
    """ Delete creditcard deletes nothing in related tables"""

    created_creditcard = random_creditcard()
    created_creditcard.delete()
    assert True if CreditCard.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if User.objects.all().count() == 1 else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_delete_creditcard_from_customer():
    """ Delete customer deletes his credit cards"""

    created_creditcard = random_creditcard()
    created_customer = created_creditcard.customer
    created_customer.delete()
    assert True if CreditCard.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 0 else False
    assert True if User.objects.all().count() == 0 else False


@pytest.mark.order(11)
@pytest.mark.django_db
def test_is_active_creditcard():
    """ The creditcard is active if expiration date has not passed """

    created_creditcard = random_creditcard()

    # one month ago
    prev_month = datetime.today().month - 1 if datetime.today().month != 1 else 12
    prev_year = datetime.today().year if datetime.today().month != 1 else datetime.today().year - 1

    # one month into the future
    next_month = datetime.today().month + 1 if datetime.today().month != 12 else 1
    next_year = datetime.today().year if datetime.today().month != 12 else datetime.today().year + 1

    # try with a good card
    created_creditcard.expire_month = next_month
    created_creditcard.expire_year = next_year
    created_creditcard.save()
    assert True if created_creditcard.is_active else False

    # try with an expired card
    created_creditcard.expire_month = prev_month
    created_creditcard.expire_year = prev_year
    created_creditcard.save()
    assert True if not created_creditcard.is_active else False





@pytest.mark.order(11)
@pytest.mark.django_db
def test_custom_creditcard():
    """ Test simple custom methods in customer """

    created_creditcard = random_creditcard()
    assert True if isinstance(str(created_creditcard), str) else False
    assert True if isinstance(created_creditcard.label, str) else False






















# expire year +20 -10
# expire month 1, 12
# security code 3 digits
# card number validation
# custom property is_active hp sp
# customer not empty







