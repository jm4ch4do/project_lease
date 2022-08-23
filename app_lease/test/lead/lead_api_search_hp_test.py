import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(4)
@pytest.mark.django_db
def test_staff_can_search_lead():
    """ Staff user can search leads """

    # create lead
    created_lead = random_lead()

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # modify lead
    created_lead.first_name = 'aaaa'
    created_lead.last_name = 'bbbb'
    created_lead.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("lead_search")
    url += '?first_name=aaa&last_name=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('last_name') == created_lead.last_name
