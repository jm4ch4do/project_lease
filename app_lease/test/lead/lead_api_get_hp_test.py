import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(4)
@pytest.mark.django_db
def test_staff_gets_any_lead_details():
    """ A staff member can get any lead details """

    # create lead
    created_lead = random_lead()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("lead_edit", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['last_name']


@pytest.mark.order(4)
@pytest.mark.django_db
def test_superuser_gets_any_lead_details():
    """ A superuser can get any lead details """

    # create lead
    created_lead = random_lead()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("lead_edit", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['last_name']
