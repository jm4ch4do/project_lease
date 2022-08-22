import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_customer_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Customer


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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_modify_own_customer_details():
    """ A regular user can modify his customer information"""

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    payload = random_customer_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("first_name")
    assert Customer.objects.first().first_name == payload["first_name"]


@pytest.mark.order(2)
@pytest.mark.django_db
def test_delete_own_customer_details():
    """ A regular user can delete his customer"""

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting customer details
    url = reverse("customer_edit", kwargs={'pk': created_customer.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Customer.objects.all().count() == 0


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_can_search_customers():
    """ Staff user can search customers """

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # create customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_customer.first_name = 'aaaa'
    created_customer.last_name = 'bbbb'
    created_customer.job = 'cccc'
    created_customer.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("customer_search")
    url += '?first_name=aaa&last_name=bbb&job=ccc&'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert Customer.objects.first().last_name == created_customer.last_name
