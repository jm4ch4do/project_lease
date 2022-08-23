import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_lead, random_user, random_lead_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Lead


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_modify_lead_details():
    """ A staff member can modify a lead information"""

    # create lead
    created_lead = random_lead()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting lead details
    url = reverse("lead_edit", kwargs={'pk': created_lead.id})
    payload = random_lead_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("first_name")
    assert Lead.objects.first().last_name == payload["last_name"]
