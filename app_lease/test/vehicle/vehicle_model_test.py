# ------------------------------ VEHICLE MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Vehicle, Customer
from app_lease.test.generator import random_vehicle
from django.contrib.auth.models import User


@pytest.mark.order(7)
@pytest.mark.django_db
def test_create_vehicle():
    """ A vehicle must be related to a customer which is related to a user """

    created_vehicle = random_vehicle()
    assert True if isinstance(created_vehicle, Vehicle) else False  # Vehicle object created
    assert True if Vehicle.objects.all().count() == 1 else False  # only one object in table vehicle
    assert True if User.objects.all().count() == 1 else False  # only one object in table users
    assert True if Customer.objects.all().count() == 1 else False  # only one object in table customer
    assert True if Vehicle.objects.first().customer.id == Customer.objects.first().id else False  # vehicle relates to customer
    assert True if Customer.objects.first().user.id == User.objects.first().id else False  # customer relates to user


@pytest.mark.order(7)
@pytest.mark.django_db
def test_delete_vehicle():
    """ Deleting vehicle deletes related customer and user """

    # deleting vehicle should not delete customer or user
    created_vehicle = random_vehicle()
    Vehicle.objects.all().delete()
    assert True if Vehicle.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if User.objects.all().count() == 1 else False


@pytest.mark.order(7)
@pytest.mark.django_db
def test_delete_vehicle_from_customer():
    """ Deleting customer also deletes user and vehicle """

    created_vehicle = random_vehicle()
    Customer.objects.all().delete()
    assert True if Customer.objects.all().count() == 0 else False
    assert True if Vehicle.objects.all().count() == 0 else False
    assert True if User.objects.all().count() == 0 else False


@pytest.mark.order(7)
@pytest.mark.django_db
def test_delete_vehicle_from_user():
    """ Deleting user also deletes customer and vehicle """

    created_vehicle = random_vehicle()
    User.objects.all().delete()
    assert True if User.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 0 else False
    assert True if Vehicle.objects.all().count() == 0 else False


@pytest.mark.order(7)
@pytest.mark.django_db
def test_custom_vehicle():
    """ testing custom methods in vehicle """

    created_vehicle = random_vehicle()
    assert True if isinstance(str(random_vehicle), str) else False  # object returns valid string
    assert True if isinstance(created_vehicle.name, str) else False  # age return valid str
