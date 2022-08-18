import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_delete_own_user():
    """ A regular user can delete his own user data """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_deletes_any_user():
    """ A staff member can delete any user """

    # create user
    created_user = random_user(is_active=1)

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
