import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_create_user():
    """ A superuser can create users of any kind """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_superuser = True
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for creating regular user
    url = reverse("user_add")
    payload = random_user_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201  # created status
    assert response.data.get("email") == payload.get("email")
    assert response.data.get("username") == payload.get("username")
    assert response.data.get('id') is not None
    assert "password" not in response.data

    # make request for creating staff user
    url = reverse("user_add")
    payload = random_user_payload()
    payload["is_staff"] = True
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201  # created status
    assert response.data.get("email") == payload.get("email")
    assert response.data.get("username") == payload.get("username")
    assert response.data.get('id') is not None
    assert "password" not in response.data

    # make request for creating superuser
    url = reverse("user_add")
    payload = random_user_payload()
    payload["is_superuser"] = True
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201  # created status
    assert response.data.get("email") == payload.get("email")
    assert response.data.get("username") == payload.get("username")
    assert response.data.get('id') is not None
    assert "password" not in response.data
