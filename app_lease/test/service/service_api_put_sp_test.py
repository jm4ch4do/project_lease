import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_service, random_user, random_service_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Service


@pytest.mark.order(6)
@pytest.mark.django_db
def test_regular_user_cant_modify_service_details():
    """ A regular user can't modify a service details"""

    # create service
    created_service = random_service()

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting service details
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    payload = random_service_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")
