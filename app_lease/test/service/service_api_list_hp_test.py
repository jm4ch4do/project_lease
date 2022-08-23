import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_service
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(6)
@pytest.mark.django_db
def test_regular_user_get_service_list():
    """ A regular user can get the list of all services """

    # create service
    created_service = random_service()

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("services")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['name']


@pytest.mark.order(6)
@pytest.mark.django_db
def test_staff_get_service_list():
    """ A staff member can get the list of all services """

    # create service
    created_service = random_service()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("services")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['name']\


@pytest.mark.order(6)
@pytest.mark.django_db
def test_superuser_get_service_list():
    """ A superuser can get the list of all services """

    # create service
    created_service = random_service()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("services")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['name']
