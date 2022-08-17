import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_gets_list_user():
    """ staff members can get the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = True
    created_user.save()

    # create related customer
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert isinstance(response.data[0]['username'], str)
    assert isinstance(response.data[0]['customer_id'], int)
    assert not response.data[0].get('password')
    assert not response.data[0].get('token')


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_gets_list_user():
    """ superusers members can get the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_superuser = True
    created_user.save()

    # create related customer
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert isinstance(response.data[0]['username'], str)
    assert isinstance(response.data[0]['customer_id'], int)
    assert not response.data[0].get('password')
    assert not response.data[0].get('token')
