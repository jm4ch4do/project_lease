import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_service
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_regular_user_can_search_service():
    """ Regular user can search services """

    # create service
    created_service = random_service()

    # create regular user
    regular_user = random_user(is_active=True)
    # modify service
    created_service.name = 'aaaa'
    created_service.service_type = 1
    created_service.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("service_search")
    url += '?name=aaa&service_type=1'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('name') == created_service.name


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_can_search_service():
    """ Staff user can search services """

    # create service
    created_service = random_service()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # modify service
    created_service.name = 'aaaa'
    created_service.service_type = 1
    created_service.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("service_search")
    url += '?name=aaa&service_type=1'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('name') == created_service.name


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_can_search_service():
    """ Superuser user can search services """

    # create service
    created_service = random_service()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # modify service
    created_service.name = 'aaaa'
    created_service.service_type = 1
    created_service.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("service_search")
    url += '?name=aaa&service_type=1'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('name') == created_service.name
