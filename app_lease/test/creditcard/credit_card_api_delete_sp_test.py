import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_creditcard, random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import CreditCard



@pytest.mark.order(11)
@pytest.mark.django_db
def test_user_cant_deletes_any_credit_card():
    """ A regular user can't delete any credit card"""

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # created regular user
    regular_user = random_user(is_active=True)

    # configure token for user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting credit card
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 401
    assert CreditCard.objects.all().count() == 1
