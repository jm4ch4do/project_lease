import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(5)
@pytest.mark.django_db
def test_invalid_field_search_in_contact_list():
    """ Invalid field in the search results in 422 error """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("contact_search")
    url += '?name=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 422
    assert len(response.data) == 1
    assert response.data['response']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_regular_user_cant_search_contacts():
    """ Regular users can't perform contact searches """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("contact_search")
    url += '?email=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
