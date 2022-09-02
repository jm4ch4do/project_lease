import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_modify_is_staff():
    """ A regular user can't modify his staff or superuser status """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    payload = random_user_payload()
    payload['is_staff'] = True
    payload['is_superuser'] = True
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert User.objects.first().is_staff is False
    assert User.objects.first().is_superuser is False

