import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_lead_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Lead


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_adds_lead():
    """ A staff member can add a lead """

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new lead
    url = reverse("leads")
    payload = random_lead_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Lead.objects.all().count() == 1
    assert Lead.objects.first().last_name == payload['last_name']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_adds_lead():
    """ A superuser member can add a lead """

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new lead
    url = reverse("leads")
    payload = random_lead_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Lead.objects.all().count() == 1
    assert Lead.objects.first().last_name == payload['last_name']
