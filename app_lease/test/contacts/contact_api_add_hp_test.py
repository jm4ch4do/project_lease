import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, \
    random_contact_payload, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Contact, Customer, Lead


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_adds_contact_for_own_customer():
    """ A regular user can add a contact for his own customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']
    assert Contact.objects.first().customer == Customer.objects.first()


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_adds_contact_for_customer():
    """ A staff member can add a contact for any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']
    assert Contact.objects.first().customer == Customer.objects.first()


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_adds_contact_for_customer():
    """ A superuser can add a contact for any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_customer, contact_type=2)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().phone == str(payload['phone'])
    assert Contact.objects.first().customer == Customer.objects.first()


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_adds_contact_for_lead():
    """ A staff member can add a contact for any lead """

    # create lead
    created_lead = random_lead()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_lead)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']
    assert Contact.objects.first().lead == Lead.objects.first()


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_adds_contact_for_lead():
    """ A superuser can add a contact for any lead """

    # create lead
    created_lead = random_lead()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_lead)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Contact.objects.all().count() == 1
    assert Contact.objects.first().email == payload['email']
    assert Contact.objects.first().lead == Lead.objects.first()
