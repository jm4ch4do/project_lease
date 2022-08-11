import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_customer_payload
from django.urls import reverse
from django.contrib.auth.models import User
from app_lease.models import Customer

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    """ A new user is able to register and gets token back, also gets customer_id """

    # make request
    url = reverse("api_register")
    payload = random_user_customer_payload()
    response = client.post(url, payload)

    # get data back
    data = response.data
    created_user = User.objects.first()
    created_customer = Customer.objects.first()

    # response has the correct values
    assert data.get("email") == payload.get("email")
    assert data.get("username") == payload.get("username")
    assert isinstance(data.get('token'), str)
    assert data.get('user_id') is not None
    assert data.get('customer_id') is not None
    assert "password" not in data
    assert data.get('response') is not None  # a response was provided
    assert response.status_code == 200
    assert len(data.keys()) == 6  # no extra values in response

    # created user is active, not_staff, not_superuser
    assert created_user.is_active
    assert not created_user.is_staff
    assert not created_user.is_superuser

    # password was encrypted before storing it
    assert created_user.check_password(payload["password"])

    # created customer is active, and is linked to user
    assert created_customer.status == 1
    assert created_customer.user == created_user







# user is able to change password using old password
# user is able to reset passwords
# new view to create staff members that can only be accessed by superuser



# User login
# correct user and password gives you token
# incorrect gives you error (403 Invalid Credentials)
# token is returned together on user login

# tokens are not returned in user list or user view data,
# passwords are never returned

# response.status_code must be always correct


# only staff and superuser can get user list

# each user can view, delete, modify, their own user
# staff or superuser can do the same on any user




