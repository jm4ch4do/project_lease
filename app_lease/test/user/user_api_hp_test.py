import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_user_customer_payload, random_customer
from django.urls import reverse
from django.contrib.auth.models import User
from app_lease.models import Customer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token



@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_user():
    """ A new user is able to register and gets token back, also gets customer_id """

    # make request
    client = APIClient()
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
    assert response.status_code == 201  # created status
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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_own_user():
    """ A user can update his own password, also staff members and superuser can """

    # create user with related customer
    created_user = random_user(is_active=1)
    created_customer = random_customer(user=created_user)

    # configure token
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for changing password
    new_password = "NewPassword123"
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response is correct
    assert response.data.get('response') is not None
    assert response.status_code == 200

    # verify password was indeed changed correctly
    assert User.objects.first().check_password(new_password)


@pytest.mark.skip
@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_staff_user():
    """ A staff member can can update any user's password"""
    pass


@pytest.mark.skip
@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_superuser_user():
    """ A superuser can can update any user's password"""
    pass





# authenticate user
# user = authenticate(username=created_user.username, password='mypassword')
# assert False if user is None else True
# login(None, user)

# can't change password if user doesn't exist
# can't change password if user is not authenticated
# can't change password if user has no permission to modify (user, staff or superuser)
# new password can't be empty
# not active user should be refused




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




