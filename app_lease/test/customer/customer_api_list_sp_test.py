import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_get_customer_list():
    """ A regular user can't get the list of all customers """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for customer list
    url = reverse("customers")
    payload = random_customer_payload()
    response = client.get(url, payload)

    # response has the correct values
    assert response.status_code == 401  # created status
    assert response.data.get("response")
