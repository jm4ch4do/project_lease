import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_staff_superuser():
    """ Staff member can't change superuser password """

    # create user who is superuser
    created_user = random_user(is_active=1)
    created_user.is_superuser = 1
    created_user.save()

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = 1
    staff_user.save()

    # configure token for superuser
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for changing password
    new_password = "NewPassword123"
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response 401
    assert response.data.get('response') is not None
    assert response.status_code == 401

    # verify password was not updated
    assert not User.objects.first().check_password(new_password)


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_user_user():
    """ User member can't change another user's password """

    # create user
    created_user = random_user(is_active=1)

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = 1
    staff_user.save()

    # delete user
    deleted_user_id = created_user.pk
    created_user.delete()

    # configure token for superuser
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for changing password
    new_password = "NewPassword123"
    url = reverse('api_password_update', kwargs={'pk': deleted_user_id})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response 401
    assert response.data.get('response') is not None
    assert response.status_code == 404


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_no_existing_user():
    """ Password can't be changed if user doesn't exists """

    # create user
    created_user = random_user(is_active=1)

    # create another user
    simple_user = random_user(is_active=1)

    # configure token for superuser
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=simple_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for changing password
    new_password = "NewPassword123"
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response 401
    assert response.data.get('response') is not None
    assert response.status_code == 401

    # verify password was not updated
    assert not User.objects.first().check_password(new_password)


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_not_authenticated():
    """ Password can't be changed if user is not authenticated """

    # create user
    created_user = random_user(is_active=1)

    # configure token for user
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=created_user)

    # make request for changing password
    new_password = "NewPassword123"
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response 401
    assert response.data.get('response') is not None
    assert response.status_code == 401

    # verify password was not updated
    assert not User.objects.first().check_password(new_password)


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_empty_password():
    """ New password can't be empty """

    # create user
    created_user = random_user(is_active=1)

    # configure token for user
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for changing password
    new_password = ""
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response 400
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # verify password was not updated
    assert not User.objects.first().check_password(new_password)


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_weak_password():
    """
    API refuses to update if password is weak. Password must include:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
     """

    # create user
    created_user = random_user(is_active=1)

    # configure token for user
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})

    # error because password is too short
    payload = dict(password="Tdo123*")
    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no digits
    payload = dict(password="TecladoABC*")
    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no lowercase
    payload = dict(password="TECLADO123*")
    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no uppercase
    payload = dict(password="teclado123*")
    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password doesn't have symbols
    payload = dict(password="Teclado123")
    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')


@pytest.mark.order(2)
@pytest.mark.django_db
def test_password_cant_update_inactive_user():
    """ A user can't update any password if inactive """

    # create user
    created_user = random_user()
    created_user.is_active = False
    created_user.save()

    # configure token for user
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for changing password
    new_password = "NewPassword123*"
    url = reverse('api_password_update', kwargs={'pk': created_user.pk})
    payload = dict(password=new_password)
    response = client.put(url, payload)

    # verify response 400
    assert response.status_code == 401

    # verify password was not updated
    assert not User.objects.first().check_password(new_password)

    # ----- same goes for superuser
    # create superuser
    super_user = random_user()
    super_user.is_active = False
    super_user.is_superuser = True
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

    # verify response 400
    assert response.status_code == 401

    # verify password was not updated
    assert not User.objects.first().check_password(new_password)
