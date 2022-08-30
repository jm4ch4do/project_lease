import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, \
    random_contact_payload, random_contact, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Contact


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_modifies_contact_for_own_customer():
    """ A regular user can modify a contact for his own customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_customer)
    del payload['customer']
    del payload['lead']
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_modifies_contact_for_any_customer():
    """ A staff user can modify a contact for any customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_customer)
    del payload['customer']
    del payload['lead']
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_modifies_contact_for_any_customer():
    """ A superuser user can modify a contact for any customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create super user
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for supser user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_customer)
    del payload['customer']
    del payload['lead']
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_modifies_contact_for_lead():
    """ A staff member can modify a contact for any lead """

    # create lead and contact
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_lead)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_modifies_contact_for_lead():
    """ A superuser can modify a contact for any lead """

    # create lead and contact
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to modify contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    payload = random_contact_payload(owner=created_lead)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']
