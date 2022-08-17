import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_empty_search():
    """ Empty search returns 204 error """

    # create user
    staff_user = random_user(is_active=1)
    staff_user.username = "aaaa"
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?username=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 204
    assert len(response.data) == 1
    assert response.data['response']

# regular user can't perform search
# invalid search fields are reported with error 422