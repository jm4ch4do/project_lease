import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_contact, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_user_cant_get_contacts_for_any_lead():
    """ A regular user can't get the contacts for any lead """

    # create lead with two contacts
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)
    created_contact2 = random_contact(related_to='lead', owner=created_lead)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_lead", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_non_auth_superuser_cant_get_contacts_for_any_lead():
    """ A superuser can't get the contacts for a lead if not authenticated """

    # create user, customer and two contacts
    # create lead with two contacts
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)
    created_contact2 = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_lead", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_cant_get_contacts_of_non_existent_lead():
    """ When superuser tries to get contacts of non-existent lead it will
        obtain a 404 error """

    # create lead with two contacts
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)
    created_contact2 = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_lead", kwargs={'pk': created_lead.id})
    created_lead.delete()
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data['response']
