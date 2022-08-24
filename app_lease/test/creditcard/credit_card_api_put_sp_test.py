import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_creditcard, random_creditcard_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import CreditCard


@pytest.mark.order(11)
@pytest.mark.django_db
def test_user_cant_modify_any_credit_card_details():
    """ A regular user can't modify another customer credit card's information"""

    # create regular user
    regular_user = random_user(is_active=True)

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting credit card details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    payload = random_creditcard_payload(customer=created_customer)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")
