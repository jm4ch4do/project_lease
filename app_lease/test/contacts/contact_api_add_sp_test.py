import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_contact_payload, random_user, \
    random_customer, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Contact


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_cant_adds_contact_for_any_customer():
    """ A regular user can't add a contact for any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_cant_add_contact_for_lead():
    """ A regular user can't add a contact for a lead """

    # create lead
    created_lead = random_lead()

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_lead)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_cant_add_any_vehicle():
    """ A regular user can't add a vehicle to another customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values



@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_cant_add_vehicle_for_deleted_customer():
    """ A staff member (or superuser) can't add a vehicle to a non-existent customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_customer_id = created_customer.id
    created_customer.delete()

    # create staff member
    staff_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload()
    payload['customer'] = created_customer_id
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Vehicle.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_add_contact_for_lead_if_not_authenticated():
    """ A superuser can't add a contact for a lead if not authenticated"""

    # create lead
    created_lead = random_lead()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add contact for created customer
    url = reverse("contacts")
    payload = random_contact_payload(owner=created_lead)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_add_contact_for_lead_if_not_active():
    """ A superuser can't add a contact for a lead if not active """

    # create lead
    created_lead = random_lead()

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.is_active = False
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
    assert response.status_code == 401
    assert response.data.get('detail')
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_set_both_lead_and_customer_for_a_contact():
    """ A superuser can't set both lead and customer for a contact """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create lead
    created_lead = random_lead()

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
    payload['lead'] = created_lead.id
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_leave_blank_both_lead_and_customer_for_a_contact():
    """ A superuser can't leave blank both lead and customer for a contact """

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
    payload['lead'] = ""
    payload['customer'] = ""
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_set_both_phone_and_email_for_a_contact():
    """ A superuser can't set both phone and email for a contact """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create lead
    created_lead = random_lead()

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
    payload['email'] = 'testingemail@gmail.com'
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_cant_leave_blank_both_phone_and_email_for_a_contact():
    """ A superuser can't leave blank both phone and email for a contact """

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
    payload['phone'] = ""
    payload['email'] = ""
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Contact.objects.all().count() == 0
