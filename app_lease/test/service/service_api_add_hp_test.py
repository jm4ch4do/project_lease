import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_service_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Service


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_adds_service():
    """ A staff member can add a service """

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new service
    url = reverse("services")
    payload = random_service_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Service.objects.all().count() == 1
    assert Service.objects.first().name == payload['name']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_adds_service():
    """ A superuser can add a service """

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new service
    url = reverse("services")
    payload = random_service_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Service.objects.all().count() == 1
    assert Service.objects.first().name == payload['name']
