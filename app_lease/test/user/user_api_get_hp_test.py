import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_get_own_user_details():
    """ A regular user can get his own user data """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email")
    assert response.data.get("username")
    assert response.data.get("is_active") is not None
    assert response.data.get("is_staff") is not None
    assert response.data.get("customer_id") is not None
    assert response.data.get('id')
    assert "password" not in response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_gets_any_user_details():
    """ A staff member can get details on any user """

    # create user
    created_user = random_user(is_active=1)

    # create staff
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email")
    assert response.data.get("username")
    assert response.data.get("is_active") is not None
    assert response.data.get("is_staff") is not None
    assert response.data.get("customer_id") is not None
    assert response.data.get('id')
    assert "password" not in response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_gets_any_user_details():
    """ A superuser can get details on any user """

    # create user
    created_user = random_user(is_active=1)

    # create superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email")
    assert response.data.get("username")
    assert response.data.get("is_active") is not None
    assert response.data.get("is_staff") is not None
    assert response.data.get("customer_id") is not None
    assert response.data.get('id')
    assert "password" not in response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_gets_any_superuser_details():
    """ A superuser can get details on any superuser """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_superuser = True
    created_user.save()

    # create superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email")
    assert response.data.get("username")
    assert response.data.get("is_active") is not None
    assert response.data.get("is_staff") is not None
    assert response.data.get("customer_id") is not None
    assert response.data.get('id')
    assert "password" not in response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_gets_any_staff_details():
    """ A superuser can get details on any staff member """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = 1
    created_user.save()

    # create superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = 1
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email")
    assert response.data.get("username")
    assert response.data.get("is_active") is not None
    assert response.data.get("is_staff") is not None
    assert response.data.get("customer_id") is not None
    assert response.data.get('id')
    assert "password" not in response.data
