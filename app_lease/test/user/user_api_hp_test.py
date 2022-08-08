import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload

client = APIClient()


@pytest.mark.django_db
def test_register_user():

    url = "/api/register/"
    payload = random_user_payload()

    response = client.post(url, payload)
    data = response.data

    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert "password" not in data
