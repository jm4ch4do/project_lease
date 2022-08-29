import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_contact, random_user, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Contact


@pytest.mark.order(5)
@pytest.mark.django_db
def test_regular_user_cant_delete_contact_for_a_lead():
    """ A regular user can't delete a contact for belonging to a lead """

    # create lead
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create regular user
    created_user = random_user(is_active=True)

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 401
    assert Contact.objects.all().count() == 1


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_delete_contact_for_lead_if_not_authenticated():
    """ A superuser can't add a contact for a lead if not authenticated"""

    # create lead with contact
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Contact.objects.all().count() == 1


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_delete_contact_for_lead_if_not_active():
    """ A superuser can't add a contact for a lead if not active """

    # create lead
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.is_active = False
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('detail')
    assert Contact.objects.all().count() == 1
