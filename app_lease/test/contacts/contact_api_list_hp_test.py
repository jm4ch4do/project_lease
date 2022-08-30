import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_gets_contact_list_for_own_customer():
    """ A regular user can get the list of all contacts for his own customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create regular user, customer and contact
    regular_user = random_user(is_active=True)
    regular_customer = random_customer(user=regular_user)
    regular_contact = random_contact(owner=regular_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("contacts")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == regular_contact.id
    assert response.data[0]['customer']
    assert response.data[0]['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_gets_contact_list():
    """ A staff member can get the list of all contacts """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("contacts")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['customer']
    assert response.data[0]['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_gets_contact_list():
    """ A superuser can get the list of all contacts """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("contacts")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['customer']
    assert response.data[0]['email']
