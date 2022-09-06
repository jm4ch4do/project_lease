import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_service,\
    random_vehicle, random_trade
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Trade


@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete_own_trade():
    """ A regular user can delete his own trade """

    # create user, customer, service, vehicle, service and trade
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()
    created_trade = random_trade(service=created_service, vehicle=created_vehicle)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting trade
    url = reverse("trade_edit", kwargs={'pk': created_trade.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Trade.objects.all().count() == 0
