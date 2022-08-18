import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_cant_get_details_staff():
    """ A staff can't get details of another staff """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = True
    created_user.save()

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_cant_get_details_superuser():
    """ A staff can't get details of another superuser """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_superuser = True
    created_user.save()

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")



@pytest.mark.order(2)
@pytest.mark.django_db
def test_cant_get_user_details_if_not_authenticated():
    """ Can't get user details if not authenticated """

    # create user
    created_user = random_user(is_active=1)
    created_user.save()

    # configure token for staff_user
    client = APIClient()

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_cant_get_user_that_doesnt_exist():
    """ Can't get user that doesn't exist """

    # create user
    created_user = random_user(is_active=1)

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # delete user
    created_user_id = created_user.id
    created_user.delete()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user_id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_get_any_user():
    """ A user can't get anothers user information """

    # create user
    created_user = random_user(is_active=1)

    # create staff member
    another_user = random_user(is_active=1)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=another_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")
