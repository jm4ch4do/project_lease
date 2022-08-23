import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_lead, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Lead


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_deletes_lead():
    """ A staff user can delete any lead"""

    # create lead
    created_lead = random_lead()

    # create vehicle with active customer and user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting lead
    url = reverse("lead_edit", kwargs={'pk': created_lead.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Lead.objects.all().count() == 0
