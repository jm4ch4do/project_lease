import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_service, random_user, random_service_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Service


@pytest.mark.order(6)
@pytest.mark.django_db
def test_staff_modify_service_details():
    """ A staff member can modify a service details"""

    # create service
    created_service = random_service()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting service details
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    payload = random_service_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("name")
    assert Service.objects.first().name == payload["name"]


@pytest.mark.order(6)
@pytest.mark.django_db
def test_staff_modify_service_details():
    """ A superuser can modify a service details"""

    # create service
    created_service = random_service()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting service details
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    payload = random_service_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("name")
    assert Service.objects.first().name == payload["name"]
