import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_vehicle_payload, random_user, random_customer, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Vehicle


@pytest.mark.order(7)
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


@pytest.mark.order(7)
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


@pytest.mark.order(7)
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


@pytest.mark.order(7)
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
