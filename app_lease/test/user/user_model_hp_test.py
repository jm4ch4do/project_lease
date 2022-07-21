# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Customer
from app_lease.test.utils import random_user, random_customer
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_user():
    created_user = random_user()
    assert True if isinstance(created_user, User) else False  # User object created
    assert True if User.objects.all().count() == 1 else False  # only one object in table users
    assert True if Customer.objects.all().count() == 0 else False  # customers should be empty


@pytest.mark.django_db
def test_delete_user():
    # deleting user should delete user and customer
    created_customer = random_customer()
    User.objects.all().delete()
    assert True if User.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 0 else False
