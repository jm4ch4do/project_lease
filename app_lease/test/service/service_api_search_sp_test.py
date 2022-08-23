import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_service
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_invalid_field_search_in_service_list():
    """ Invalid field in the search results in 422 error """

    # create service
    created_service = random_service()

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("service_search")
    url += '?email=aaa'
    response = client.get(url)

    # get data back
    assert response.status_code == 422
    assert len(response.data) == 1
    assert response.data['response']
