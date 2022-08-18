import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer_payload, random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_fail_customer_create():
    """ Customer can't be created directly using the API.
        To create a customer you must register a user
    """

    # create super_user
    super_user = random_user(is_active=1)
    super_user.is_superuser = True
    super_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for creating customer
    url = reverse("customers")
    payload = random_customer_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 405  # created status
    assert response.data.get("detail")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_get_customer_list():
    """ A regular user can't get the list of all customers """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for customer list
    url = reverse("customers")
    payload = random_customer_payload()
    response = client.get(url, payload)

    # response has the correct values
    assert response.status_code == 401  # created status
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_get_another_user_details():
    """ A regular user can't get another customer's data """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_not_authenticated_superuser_cant_get_another_user_details():
    """ A superuser needs to authenticate to get a customer's data """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get("response")


@pytest.mark.order(2)
@pytest.mark.django_db
def test_cant_get_details_of_non_existent_customer():
    """ When superuser tries to get details of non-existent customer it will
        obtain a 404 error """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # delete customer
    created_customer_id = created_customer.id
    created_customer.delete()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer_id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data.get("response")


# each user can get his own customer
# staff and superuser can get any customer
# only staff and superuser can get all customers