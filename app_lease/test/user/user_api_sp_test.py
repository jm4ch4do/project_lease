import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_customer_payload, random_user
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_fails_duplicated_user():
    """ Refuses to created duplicated username or email, returns 400 """

    # constants
    url = reverse("api_register")

    # one user registers
    payload = random_user_customer_payload()
    client = APIClient()
    response = client.post(url, payload)

    # a second user tries to use same username to register
    payload2 = random_user_customer_payload()
    payload2['username'] = payload['username']
    response = client.post(url, payload2)

    # response is an error
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert not response.data.get('password')

    # a third user tries to use same email to register
    payload3 = random_user_customer_payload()
    payload3['email'] = payload['username']
    response = client.post(url, payload3)

    # response is an error again
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert not response.data.get('password')


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_fails_empty_username():
    """ System refuses to register if username is empty """

    # constants
    url = reverse("api_register")

    # a user tries to register with empty name
    payload = random_user_customer_payload()
    client = APIClient()
    payload['username'] = ""
    response = client.post(url, payload)

    # response is an error
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('username')


@pytest.mark.order(2)
@pytest.mark.django_db
def test_register_fails_weak_password():
    """
    API refuses to update if password is weak. Password must include:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
     """
    # constants
    url = reverse("api_register")

    # a user tries to register with empty name
    payload = random_user_customer_payload()
    client = APIClient()

    # error because password is too short
    payload['password'] = "Tdo123*"
    payload['password2'] = "Tdo123*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no digits
    payload['password'] = "TecladoABC"
    payload['password2'] = "TecladoABC"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no lowercase
    payload['password'] = "TECLADO123*"
    payload['password2'] = "TECLADO123*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password has no uppercase
    payload['password'] = "teclado123*"
    payload['password2'] = "teclado123*"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')

    # error because password doesn't have symbols
    payload['password'] = "Teclado123"
    payload['password2'] = "Teclado123"
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not response.data.get('token')
    assert response.data.get('password')


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

    # make request for changing password with missing special characters
    new_password = "Teclado123"
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



@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_username_cant_be_empty():
    """ A user can't log in with empty username """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": "", "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_password_cant_be_empty():
    """ A user can't log in with empty password """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": ""}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_fails_due_to_bad_password():
    """ A user can't log if his password is wrong """

    # create user
    created_user = random_user(is_active=1)
    new_password = 'somerandomwrongpassword123*'

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_fails_due_to_bad_username():
    """ A user can't log if his username is wrong """

    # create user
    created_user = random_user(is_active=1)
    new_username = 'somerandomwrongusername123'
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": new_username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data


@pytest.mark.order(2)
@pytest.mark.django_db
def test_login_fails_for_inactive_user():
    """ A user can't login if it's inactive """

    # create user
    created_user = random_user(is_active=True)
    created_user.is_active = False
    new_password = 'mypassword123'
    created_user.set_password(new_password)
    created_user.save()

    # make request
    client = APIClient()
    url = reverse("api_login")
    payload = {"username": created_user.username, "password": new_password}
    response = client.post(url, payload)

    # get data back
    assert response.status_code == 400
    assert response.data
