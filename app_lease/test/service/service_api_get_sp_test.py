import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_service
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_not_authenticated_superuser_cant_get_service_details():
    """ A superuser needs to authenticate to get a service's details """

    # create service
    created_service = random_service()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("lead_edit", kwargs={'pk': created_service.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_cant_get_details_of_non_existent_service():
    """ When superuser tries to get details of non-existent service it will
        obtain a 404 error """

    # create service
    created_service = random_service()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # delete service
    created_service_id = created_service.id
    created_service.delete()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("service_edit", kwargs={'pk': created_service_id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data.get("response")
