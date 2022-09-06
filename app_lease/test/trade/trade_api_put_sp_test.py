import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_service,\
    random_trade, random_vehicle, random_trade_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Trade


@pytest.mark.order(8)
@pytest.mark.django_db
def test_user_cant_modify_any_trade_details():
    """ A regular user can't modify any trade """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("trade_edit", kwargs={'pk': created_trade.id})
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Trade.objects.first().note != payload["note"]
