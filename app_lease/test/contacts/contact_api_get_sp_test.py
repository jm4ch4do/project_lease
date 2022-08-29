import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_cant_gets_contact_for_any_customer():
    """ A regular user can't get a contact for any customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to get contact
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_not_authenticated_superuser_cant_get_contact_details():
    """ A superuser needs to authenticate to get a contact data """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to get contact
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(5)
@pytest.mark.django_db
def test_cant_get_details_of_non_existent_contact():
    """ When superuser tries to get details of non-existent contact it will
        obtain a 404 error """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # delete contact
    created_contact_id = created_contact.id
    created_contact.delete()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("contact_edit", kwargs={'pk': created_contact_id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data.get("response")
