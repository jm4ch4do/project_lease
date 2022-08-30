import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_user_gets_contacts_for_own_customer():
    """ A regular user can get the contacts for his own customer """

    # create user, customer and two contacts
    created_contact = random_contact()
    created_customer = created_contact.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()
    created_contact2 = random_contact(owner=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all contacts for the customer
    url = reverse("contacts_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.order(7)
@pytest.mark.django_db
def test_staff_gets_contacts_for_any_customer():
    """ A staff member can get the contacts for any customer """

    # create user, customer and two contacts
    created_contact = random_contact()
    created_customer = created_contact.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()
    created_contact2 = random_contact(owner=created_customer)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.order(7)
@pytest.mark.django_db
def test_superuser_gets_contacts_for_any_customer():
    """ A superuser can get the contacts for any customer """

    # create user, customer and two contacts
    created_contact = random_contact()
    created_customer = created_contact.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()
    created_contact2 = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("contacts_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert len(response.data) == 2
