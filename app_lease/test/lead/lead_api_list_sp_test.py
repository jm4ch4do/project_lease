import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_get_lead_list():
    """ A regular user can't get the list of all leads """

    # create lead
    random_lead()

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for lead list
    url = reverse("vehicles")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']
