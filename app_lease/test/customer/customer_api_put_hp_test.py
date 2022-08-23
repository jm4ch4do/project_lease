import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_customer_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Customer


@pytest.mark.order(2)
@pytest.mark.django_db
def test_modify_own_customer_details():
    """ A regular user can modify his customer information"""

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    payload = random_customer_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("first_name")
    assert Customer.objects.first().first_name == payload["first_name"]
