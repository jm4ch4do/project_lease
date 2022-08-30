import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_get_customer_list():
    """ A staff member can get the list of all customers """

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # create customer
    random_customer()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for customer list
    url = reverse("customers")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['user']
    assert response.data[0]['first_name']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_get_customer_list():
    """ A superuser can get the list of all customers """

    # create superuser
    super_user = random_user(is_active=1)
    super_user.is_staff = True
    super_user.save()

    # create customer
    random_customer()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for customer list
    url = reverse("customers")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['user']
    assert response.data[0]['first_name']
