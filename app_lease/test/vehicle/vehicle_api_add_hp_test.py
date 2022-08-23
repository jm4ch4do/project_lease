import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_vehicle_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Vehicle


@pytest.mark.order(7)
@pytest.mark.django_db
def test_user_adds_own_vehicle():
    """ A regular user can add his own vehicle"""

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Vehicle.objects.all().count() == 1
    assert Vehicle.objects.first().model == payload['model']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_adds_any_vehicle():
    """ A staff member can add a vehicle to any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Vehicle.objects.all().count() == 1
    assert Vehicle.objects.first().model == payload['model']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_superuser_adds_any_vehicle():
    """ A superuser can add a vehicle to any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Vehicle.objects.all().count() == 1
    assert Vehicle.objects.first().model == payload['model']
