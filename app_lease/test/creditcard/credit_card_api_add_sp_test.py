import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_creditcard_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import CreditCard


@pytest.mark.order(11)
@pytest.mark.django_db
def test_user_cant_add_any_credit_card():
    """ A regular user can add a credit card for another user """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new credit card
    url = reverse("credit_cards")
    payload = random_creditcard_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert CreditCard.objects.all().count() == 0
