import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_customer_payload
from django.urls import reverse
from django.contrib.auth.models import User
from app_lease.models import Customer


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_user():
    """ A new user is able to register and gets token back, also gets customer_id """

    # make request
    client = APIClient()
    url = reverse("api_register")
    payload = random_user_customer_payload()
    response = client.post(url, payload)

    # get data back
    data = response.data
    created_user = User.objects.first()
    created_customer = Customer.objects.first()

    # response has the correct values
    assert data.get("email") == payload.get("email")
    assert data.get("username") == payload.get("username")
    assert isinstance(data.get('token'), str)
    assert data.get('user_id') is not None
    assert data.get('customer_id') is not None
    assert "password" not in data
    assert data.get('response') is not None  # a response was provided
    assert response.status_code == 201  # created status
    assert len(data.keys()) == 6  # no extra values in response

    # created user is active, not_staff, not_superuser
    assert created_user.is_active
    assert not created_user.is_staff
    assert not created_user.is_superuser

    # password was encrypted before storing it
    assert created_user.check_password(payload["password"])

    # created customer is active, and is linked to user
    assert created_customer.status == 1
    assert created_customer.user == created_user
