import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_contact, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_gets_contacts_for_any_lead():
    """ A staff member can get the contacts for any lead """

    # create lead with two contacts
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)
    created_contact2 = random_contact(related_to='lead', owner=created_lead)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_lead", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.order(7)
@pytest.mark.django_db
def test_superuser_gets_contacts_for_any_lead():
    """ A superuser can get the contacts for any lead """

    # create lead with two contacts
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)
    created_contact2 = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_lead", kwargs={'pk': created_lead.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2
