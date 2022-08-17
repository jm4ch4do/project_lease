import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_create_user():
    """ A superuser can create users of any kind """

    # create regular user
    created_user = random_user(is_active=1)
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for creating a new regular user
    url = reverse("user_add")
    payload = random_user_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")

    # create staff user
    staff_user = random_user(is_active=1)
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for creating a new regular user
    url = reverse("user_add")
    payload = random_user_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")





# regular users and staff users can't access
# errors are shown for missing fields