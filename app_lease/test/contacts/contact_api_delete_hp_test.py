import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_contact, random_customer,\
    random_user, random_lead
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Contact


@pytest.mark.order(5)
@pytest.mark.django_db
def test_user_deletes_contact_for_own_customer():
    """ A regular user can delete a contact for his own customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_deletes_contact_for_any_customer():
    """ A staff member can delete a contact for any customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_deletes_contact_for_any_customer():
    """ A superuser can delete a contact for any customer """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_deletes_contact_for_any_lead():
    """ A staff member can delete a contact for any lead """

    # create lead
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

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert Contact.objects.all().count() == 0


@pytest.mark.order(5)
@pytest.mark.django_db
def test_superuser_deletes_contact_for_any_lead():
    """ A superuser can delete a contact for any lead """

    # create lead
    created_lead = random_lead()
    created_contact = random_contact(related_to='lead', owner=created_lead)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to delete contact for created customer
    url = reverse("contact_edit", kwargs={'pk': created_contact.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert Contact.objects.all().count() == 0
