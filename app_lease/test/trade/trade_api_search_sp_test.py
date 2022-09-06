import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_vehicle, random_customer, \
    random_service, random_trade
from django.urls import reverse


@pytest.mark.order(8)
@pytest.mark.django_db
def test_invalid_field_search_in_vehicle_list():
    """ Invalid field in the search results in 422 error """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # modify trade
    created_trade.status = 1
    created_trade.note = 'aaaa'
    created_trade.save()

    # configure request
    client = APIClient()

    # make request
    url = reverse("trade_search")
    url += '?mode=1&note=aaa'
    response = client.get(url)

    # get data back
    assert response.status_code == 422
    assert response.data['response']
