import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Customer


@pytest.mark.order(2)
@pytest.mark.django_db
def test_delete_own_customer_details():
    """ A regular user can delete his customer"""

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Customer.objects.all().count() == 0
