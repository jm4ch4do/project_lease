import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer_payload, random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Customer


@pytest.mark.order(2)
@pytest.mark.django_db
def test_search_ignores_inactive_customers_in_list():
    """ Only active customers should be in the search results """

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # create customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_customer.first_name = 'aaaa'
    created_customer.save()

    # create inactive customer
    inactive_user = random_user(is_active=False)
    inactive_customer = random_customer(user=inactive_user)
    inactive_customer.first_name = 'aaaa'
    inactive_customer.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("customer_search")
    url += '?first_name=aaa'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert Customer.objects.first().last_name == created_customer.last_name


@pytest.mark.order(2)
@pytest.mark.django_db
def test_invalid_field_search_in_customer_list():
    """ Invalid field in the search results in 422 error """

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # create customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("customer_search")
    url += '?email=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 422
    assert len(response.data) == 1
    assert response.data['response']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_regular_user_cant_search_customers():
    """ Regular users can't perform customer searches """

    # create user
    staff_user = random_user(is_active=True)

    # create customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?first_name=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
