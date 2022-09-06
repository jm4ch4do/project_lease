import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, \
    random_vehicle, random_service, random_trade_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Trade


@pytest.mark.order(8)
@pytest.mark.django_db
def test_user_adds_own_trade():
    """ A regular user can add a trade for himself """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for adding a trade for the created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Trade.objects.all().count() == 1
    assert Trade.objects.first().service == created_service
    assert Trade.objects.first().vehicle == created_vehicle
    assert Trade.objects.first().note == payload['note']


@pytest.mark.order(8)
@pytest.mark.django_db
def test_staff_adds_any_trade():
    """ A staff member can add a trade for any customer """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for adding a trade for the created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Trade.objects.all().count() == 1
    assert Trade.objects.first().service == created_service
    assert Trade.objects.first().vehicle == created_vehicle
    assert Trade.objects.first().note == payload['note']


@pytest.mark.order(8)
@pytest.mark.django_db
def test_superuser_adds_any_trade():
    """ A superuser can add a trade for any customer """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for adding a trade for the created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Trade.objects.all().count() == 1
    assert Trade.objects.first().service == created_service
    assert Trade.objects.first().vehicle == created_vehicle
    assert Trade.objects.first().note == payload['note']
