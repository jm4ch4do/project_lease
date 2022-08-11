import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload
from django.urls import reverse

client = APIClient()


@pytest.mark.django_db
def test_register_user():

    url = reverse("api_register")
    payload = random_user_payload()

    response = client.post(url, payload)
    data = response.data

    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert isinstance(data["token"], str)
    assert "password" not in data



# count amount of values in response
# verify Customer was created and linked to user
# verify user is not type staff or superuser
# password must be encripted before storing it
# user must be active
# every value was properly assigned

# correct user and password gives you token
# incorrect gives you error (403 Invalid Credentials)

# token is returned on user creation
# token is returned together with user view data

# tokens are not returned in user list
# passwords are never returned

# response.status_code must be always correct


# new view to create staff members that can only be accessed by superuser

# only staff and superuser can get user list

# each user can view, delete, modify, their own user
# staff or superuser can do the same on any user


# fails to create duplicated name

