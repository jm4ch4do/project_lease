import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_own_user():
    """ A user can update his own password """

    # create user with related customer
    created_user = random_user(is_active=1)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_staff_user():
    """ A staff member can update any user's password"""

    # create user
    created_user = random_user(is_active=1)

    # create user as member of the staff
    staff_user = random_user(is_active=1)
    staff_user.is_staff = 1
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=staff_user)
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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_superuser_user():
    """ A superuser can update any user's password"""

    # create user
    created_user = random_user(is_active=1)

    # create user as superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = 1
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=super_user)
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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_staff_staffuser():
    """ Staff member can change staff password """

    # create user
    created_user = random_user(is_active=1)
    created_user.is_staff = 1
    created_user.save()

    # create user as staff member
    super_user = random_user(is_active=1)
    super_user.is_staff = 1
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=super_user)
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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_update_superuser_superuser():
    """ Superuser can change superuser password """

    # create user who is superuser
    created_user = random_user(is_active=1)
    created_user.is_superuser = 1
    created_user.save()

    # create another superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = 1
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=super_user)
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
