import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user
from django.urls import reverse



@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_user():
    """ A user is able to login and gets token back """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    data = response.data
    assert response.status_code == 200
    assert isinstance(data.get('token'), str)
    assert data.get('username') is not None
    assert data.get('response') is not None
