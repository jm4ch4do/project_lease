import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_get_vehicle_list():
    """ A staff member can get the list of all vehicles """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("vehicles")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['customer']
    assert response.data[0]['model']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_superuser_get_vehicle_list():
    """ A superuser can get the list of all customers """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_superuser = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("vehicles")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['customer']
    assert response.data[0]['model']
