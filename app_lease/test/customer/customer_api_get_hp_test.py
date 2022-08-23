import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_get_own_customer_details():
    """ A regular user can get his customers user data """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("user")
    assert response.data.get("first_name")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_gets_any_customer_details():
    """ A staff member can get any customer user data """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("user")
    assert response.data.get("first_name")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_gets_any_customer_details():
    """ A superuser can get any customer user data """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser= True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("user")
    assert response.data.get("first_name")
