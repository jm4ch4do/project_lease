import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_service,\
    random_trade, random_vehicle, random_trade_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Trade


@pytest.mark.order(8)
@pytest.mark.django_db
def test_user_modifies_own_trade_details():
    """ A regular user can modify his own trade """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("trade_edit", kwargs={'pk': created_trade.id})
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("note")
    assert response.data.get("status")
    assert Trade.objects.first().note == payload["note"]


@pytest.mark.order(8)
@pytest.mark.django_db
def test_staff_modifies_any_trade_details():
    """ A staff member can modify any trade """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("trade_edit", kwargs={'pk': created_trade.id})
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("note")
    assert response.data.get("status")
    assert Trade.objects.first().note == payload["note"]


@pytest.mark.order(8)
@pytest.mark.django_db
def test_superuser_modifies_any_trade_details():
    """ A superuser can modify any trade """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("trade_edit", kwargs={'pk': created_trade.id})
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("note")
    assert response.data.get("status")
    assert Trade.objects.first().note == payload["note"]
