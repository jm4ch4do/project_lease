import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer_payload, random_user, random_customer, random_creditcard
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(11)
@pytest.mark.django_db
def test_user_cant_get_credit_card_list():
    """ A regular user can't get the list of all creditcards """

    # create user, customer and creditcard
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for credit card list
    url = reverse("credit_cards")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401  # created status
    assert response.data.get("response")
