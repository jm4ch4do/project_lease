import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_contact
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(5)
@pytest.mark.django_db
def test_not_authenticated_superuser_cant_get_contact_list():
    """ A superuser needs to authenticate to get a list of contact data """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("contacts")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(5)
@pytest.mark.django_db
def test_cant_get_details_of_non_existent_contact():
    """ When superuser tries to get contact list he will obtain a 204 error
    if there are no contacts """

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_staff = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("contacts")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data['response']
