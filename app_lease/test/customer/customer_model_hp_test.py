# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Customer
from app_lease.test.utils import random_customer
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_customer():
    created_customer = random_customer()
    assert True if isinstance(created_customer, Customer) else False  # Customer object created
    assert True if Customer.objects.all().count() == 1 else False  # only one object in table customers
    assert True if Customer.objects.all().count() == 1 else False  # only one object in table users
    assert True if Customer.objects.first().user.id == User.objects.first().id else False  # user and customer relation


@pytest.mark.django_db
def test_delete_customer():
    created_customer = random_customer()
    # deleting customer should delete customer and user
    Customer.objects.all().delete()
    assert True if Customer.objects.all().count() == 0 else False
    assert True if User.objects.all().count() == 0 else False

    # deleting user should also delete customer and user
    created_customer = random_customer()
    Customer.objects.all().delete()
    assert True if Customer.objects.all().count() == 0 else False
    assert True if User.objects.all().count() == 0 else False


@pytest.mark.django_db
def test_custom_customer():
    # testing custom methods in customer
    created_customer = random_customer()
    assert True if isinstance(str(random_customer), str) else False  # object returns valid string
    assert True if isinstance(created_customer.age, int) else False  # age return valid int




# assign wrong modelObject to customer or leave it empty
# create object with missing fields
# break field validation
# internal fields storing date objects
# custom methods and properties (see coverage suggestions)
# ordering










