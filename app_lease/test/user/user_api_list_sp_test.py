import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_get_list_user():
    """ A regular user can't access the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = False
    created_user.is_superuser = False
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
    assert len(response.data) == 1


@pytest.mark.order(2)
@pytest.mark.django_db
def test_unauthenticated_staff_cant_get_list_user():
    """ Unauthenticated staff members can't get the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = True
    created_user.save()

    # create related customer
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
    assert len(response.data) == 1


@pytest.mark.order(2)
@pytest.mark.django_db
def test_unauthenticated_superuser_cant_get_list_user():
    """ Unauthenticated superusers can't get the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_superuser = True
    created_user.save()

    # create related customer
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
    assert len(response.data) == 1


@pytest.mark.order(2)
@pytest.mark.django_db
def test_inactive_staff_cant_get_list_user():
    """ Inactive staff members can't get the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = True
    created_user.is_active = True
    created_user.save()

    # create related customer
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
    assert len(response.data) == 1


@pytest.mark.order(2)
@pytest.mark.django_db
def test_inactive_superuser_cant_get_list_user():
    """ Inactive superusers members can't get the list of users """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_superuser = True
    created_user.is_active = True
    created_user.save()

    # create related customer
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)

    # make request
    url = reverse("user_list")
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
    assert len(response.data) == 1

# staff and superuser can't be inactive