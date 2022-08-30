import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_vehicle, random_customer, \
    random_service, random_trade
from django.urls import reverse


@pytest.mark.order(8)
@pytest.mark.django_db
def test_anyone_can_see_trade_details():
    """ Anyone can see a trade details """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # configure request client
    client = APIClient()

    # make request for a trade details
    url = reverse("trade_edit", kwargs={'pk': created_trade.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['status']
    assert response.data['note']
