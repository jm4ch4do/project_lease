import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_user_gets_vehicles_for_own_customer():
    """ A regular user can get the vehicles for his own customer """

    # create user, customer and two vehicles
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()
    created_vehicle = random_vehicle(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("vehicles_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_gets_vehicles_for_any_customer():
    """ A staff member can get the vehicles for his own customer """

    # create user, customer and two vehicles
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()
    created_vehicle = random_vehicle(customer=created_customer)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("vehicles_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.order(7)
@pytest.mark.django_db
def test_superuser_gets_vehicles_for_any_customer():
    """ A superuser can get the vehicles for his own customer """

    # create user, customer and two vehicles
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()
    created_vehicle = random_vehicle(customer=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("vehicles_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2
