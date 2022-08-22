import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Vehicle


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_can_search_vehicles():
    """ Staff user can search vehicles """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # modify vehicle
    created_vehicle.make = 'aaaa'
    created_vehicle.model = 'bbbb'
    created_vehicle.year = 2020
    created_vehicle.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("vehicle_search")
    url += '?make=aaa&model=bbb&year=2020&'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert Vehicle.objects.first().model == created_vehicle.model
