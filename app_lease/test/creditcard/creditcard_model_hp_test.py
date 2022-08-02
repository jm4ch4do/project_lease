import pytest
from app_lease.models import Customer, CreditCard
from app_lease.test.generator import random_creditcard
from django.contrib.auth.models import User


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


@pytest.mark.order(10)
@pytest.mark.django_db
def test_delete_creditcard():
    """ Delete creditcard deletes nothing in related tables"""

    created_creditcard = random_creditcard()
    created_creditcard.delete()
    assert True if CreditCard.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if User.objects.all().count() == 1 else False























# custom property label and str output

# create card creates customer and user


# expire year +20 -10
# expire month 1, 12
# security code 3 digits
# card number validation
# custom property is_active hp sp
# customer not empty







