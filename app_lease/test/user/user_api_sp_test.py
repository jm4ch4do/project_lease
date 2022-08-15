import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_customer_payload
from django.urls import reverse
from rest_framework import status


client = APIClient()


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_duplicated_user():
    """ Refuses to created duplicated username or email, returns 400 """

    # constants
    url = reverse("api_register")

    # one user registers
    payload = random_user_customer_payload()
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





