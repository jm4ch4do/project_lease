import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_creditcard, random_customer, random_vehicle, \
    random_trade, random_service
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_user_cant_get_trades_for_any_service():
    """ A superuser can't get the trades for any service """

    # create user, customer, service and trades
    created_service = random_service()
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_vehicle2 = random_vehicle(customer=created_customer)
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)
    created_trade2 = random_trade(service=created_service, vehicle=created_vehicle2)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # request for all trades for a service
    url = reverse("trades_for_service", kwargs={'pk': created_service.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']
