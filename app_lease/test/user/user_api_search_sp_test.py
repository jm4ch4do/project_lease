import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@pytest.mark.order(2)
@pytest.mark.django_db
def test_empty_search_in_user_list():
    """ Empty search returns 204 error """

    # create user
    staff_user = random_user(is_active=1)
    staff_user.username = "aaaa"
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?username=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 204
    assert len(response.data) == 1
    assert response.data['response']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_search_ignores_inactive_users_in_list():
    """ Search results should not include inactive users """

    # create user
    staff_user = random_user(is_active=True)
    staff_user.username = "aaaa"
    staff_user.is_staff = True
    staff_user.save()

    # create inactive user
    inactive_user = random_user(is_active=False)
    inactive_user.username = "aaaa"

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?username=aaa'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert User.objects.first().last_name == staff_user.last_name


@pytest.mark.order(2)
@pytest.mark.django_db
def test_invalid_field_search_in_user_list():
    """ Invalid field in the search results in 422 error """

    # create user
    staff_user = random_user(is_active=1)
    staff_user.username = "aaaa"
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?email=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 422
    assert len(response.data) == 1
    assert response.data['response']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_search_in_user_list():
    """ A regular user is not allowed to search users"""

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
    url = reverse("user_search")
    url += '?username=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert len(response.data) == 1
    assert response.data['response']

    # configure token without authentication
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)

    # make request
    url = reverse("user_search")
    url += '?username=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert len(response.data) == 1
    assert response.data['response']
