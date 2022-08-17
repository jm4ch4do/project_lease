import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user
from django.urls import reverse


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_username_cant_be_empty():
    """ A user can't log in with empty username """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": "", "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_password_cant_be_empty():
    """ A user can't log in with empty password """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": ""}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_fails_due_to_bad_password():
    """ A user can't log if his password is wrong """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'somerandomwrongpassword123*'

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_fails_due_to_bad_username():
    """ A user can't log if his username is wrong """

    # create user
    created_user = random_user(is_active=1)
    new_username = 'somerandomwrongusername123'
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": new_username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_fails_for_inactive_user():
    """ A user can't login if it's inactive """

    # create user
    created_user = random_user(is_active=True)
    created_user.is_active = False
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data
