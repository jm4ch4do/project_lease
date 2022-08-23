import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_service
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(6)
@pytest.mark.django_db
def test_regular_user_gets_any_service_details():
    """ A regular user can get any service details """

    # create service
    created_service = random_service()

    # create staff user
    regular_user = random_user(is_active=True)
    regular_user.is_staff = True
    regular_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['name']


@pytest.mark.order(6)
@pytest.mark.django_db
def test_staff_gets_any_service_details():
    """ A staff user can get any service details """

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

    # make request for a vehicle
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['name']


@pytest.mark.order(6)
@pytest.mark.django_db
def test_superuser_gets_any_service_details():
    """ A superuser can get any service details """

    # create service
    created_service = random_service()

    # create staff user
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['name']
