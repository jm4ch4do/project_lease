# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Customer
from app_lease.test.generator import random_user, random_customer
from django.contrib.auth.models import User


@pytest.mark.order(2)
@pytest.mark.django_db
def test_create_user():
    """ User can exist without a related customer """

    created_user = random_user()
    assert True if isinstance(created_user, User) else False  # User object created
    assert True if User.objects.all().count() == 1 else False  # only one object in table users
    assert True if Customer.objects.all().count() == 0 else False  # customers should be empty


@pytest.mark.order(2)
@pytest.mark.django_db
def test_delete_user():
    """ Deleting user deletes related customer """

    created_customer = random_customer()
    User.objects.all().delete()
    assert True if User.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 0 else False
