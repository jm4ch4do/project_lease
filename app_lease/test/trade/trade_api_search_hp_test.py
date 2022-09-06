import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_vehicle, random_customer, \
    random_service, random_trade
from django.urls import reverse


@pytest.mark.order(8)
@pytest.mark.django_db
def test_anyone_can_search_trades():
    """ Staff user can search vehicles """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_vehicle2 = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)
    created_trade2 = random_trade(service=created_service, vehicle=created_vehicle2)

    # modify trade
    created_trade.status = 1
    created_trade.note = 'aaaa'
    created_trade.save()

    # configure request
    client = APIClient()

    # make request
    url = reverse("trade_search")
    url += '?status=1&note=aaa'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('status') == created_trade.status
