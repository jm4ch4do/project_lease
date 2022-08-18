import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_modify_own_user():
    """ A regular user can edit his own user data """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    payload = random_user_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email") == payload.get("email")
    assert response.data.get("username") == payload.get("username")
    assert response.data.get('id') is not None
    assert "password" not in response.data
