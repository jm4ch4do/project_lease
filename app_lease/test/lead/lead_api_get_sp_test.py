import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(4)
@pytest.mark.django_db
def test_user_cant_get_lead_details():
    """ A regular user can't get a lead details """

    # create lead
    created_lead = random_lead()

    # create user
    created_user = random_user(is_active=True)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a lead
    url = reverse("lead_edit", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(4)
@pytest.mark.django_db
def test_not_authenticated_superuser_cant_get_lead_details():
    """ A superuser needs to authenticate to get a lead's details """

    # create lead
    created_lead = random_lead()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("lead_edit", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(4)
@pytest.mark.django_db
def test_cant_get_details_of_non_existent_lead():
    """ When superuser tries to get details of non-existent lead it will
        obtain a 404 error """

    # create lead
    created_lead = random_lead()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # delete lead
    created_lead_id = created_lead.id
    created_lead.delete()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("lead_edit", kwargs={'pk': created_lead_id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data.get("response")
