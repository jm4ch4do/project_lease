import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_customer_payload, random_user
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_fails_duplicated_user():
    """ Refuses to created duplicated username or email, returns 400 """

    # constants
    url = reverse("api_register")

    # one user registers
    payload = random_user_customer_payload()
    client = APIClient()
    response = client.post(url, payload)

    # a second user tries to use same username to register
    payload2 = random_user_customer_payload()
    payload2['username'] = payload['username']
    response = client.post(url, payload2)

    # response is an error
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert not response.data.get('password')

    # a third user tries to use same email to register
    payload3 = random_user_customer_payload()
    payload3['email'] = payload['username']
    response = client.post(url, payload3)

    # response is an error again
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert not response.data.get('password')


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_fails_empty_username():
    """ System refuses to register if username is empty """

    # constants
    url = reverse("api_register")

    # a user tries to register with empty name
    payload = random_user_customer_payload()
    client = APIClient()
    payload['username'] = ""
    response = client.post(url, payload)

    # response is an error
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('username')


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_fails_weak_password():
    """
    API refuses to update if password is weak. Password must include:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
     """
    # constants
    url = reverse("api_register")

    # a user tries to register with empty name
    payload = random_user_customer_payload()
    client = APIClient()

    # error because password is too short
    payload['password'] = "Tdo123*"
    payload['password2'] = "Tdo123*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no digits
    payload['password'] = "TecladoABC*"
    payload['password2'] = "TecladoABC*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no lowercase
    payload['password'] = "TECLADO123*"
    payload['password2'] = "TECLADO123*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no uppercase
    payload['password'] = "teclado123*"
    payload['password2'] = "teclado123*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password doesn't have symbols
    payload['password'] = "Teclado123"
    payload['password2'] = "Teclado123"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')
