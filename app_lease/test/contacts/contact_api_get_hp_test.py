import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_gets_contact_for_own_customer():
    """ A regular user can get a contact for his own customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to get contact
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['customer']
    assert response.data['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_gets_contact_for_any_customer():
    """ A staff member can get a contact for any customer """

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

    # make request to get contact
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['customer']
    assert response.data['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_gets_contact_for_any_customer():
    """ A superuser can get a contact for any customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to get contact
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['customer']
    assert response.data['email']
