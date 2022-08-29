import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_contact_payload, random_user, \
    random_customer, random_lead, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Contact


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_cant_modify_contact_for_any_customer():
    """ A regular user can't modify a contact for any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_customer)
    del payload['customer']
    del payload['lead']
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Contact.objects.all().count() == 1
    assert response.data['response']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_cant_modify_contact_for_lead():
    """ A regular user can't modify a contact for a lead """

    # create lead
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_lead)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Contact.objects.all().count() == 1
    assert response.data['response']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_cant_modify_contact_for_deleted_customer():
    """ A staff member (or superuser) can't modify a contact for
     a non-existent customer """

    # create and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create staff member
    staff_user = random_user(is_active=True)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_customer)
    created_contact.delete()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 404
    assert Contact.objects.all().count() == 0
    assert response.data['response']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_modify_contact_for_lead_if_not_authenticated():
    """ A superuser can't add a contact for a lead if not authenticated"""

    # create lead
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

    # make request to modify contact for created lead
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_lead)
    del payload['customer']
    del payload['lead']
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Contact.objects.all().count() == 1
