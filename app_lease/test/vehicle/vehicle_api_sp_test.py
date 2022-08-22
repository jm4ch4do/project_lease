import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_vehicle_payload, random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Customer, Vehicle



@pytest.mark.order(2)
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
    assert response.status_code == 401
    assert Vehicle.objects.all().count() == 0


@pytest.mark.order(2)
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


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_cant_add_vehicle_if_not_authenticated():
    """ A staff member (or superuser) can't add vehicle if not authenticated """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_customer_id = created_customer.id

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload()
    payload['customer'] = created_customer_id
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Vehicle.objects.all().count() == 0


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_cant_add_vehicle_for_inactive_user():
    """ A staff member (or superuser) can't add vehicle for an inactive user """

    # create active customer
    created_user = random_user()
    created_customer = random_customer(user=created_user)
    created_user.is_active = False
    created_user.save()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 404
    assert response.data.get('response')
    assert Vehicle.objects.all().count() == 0



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
    url = reverse("user_search")
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
