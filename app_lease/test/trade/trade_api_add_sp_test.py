import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_service, random_user, random_customer,\
    random_trade_payload, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Trade


@pytest.mark.order(8)
@pytest.mark.django_db
def test_user_cant_add_any_trade():
    """ A regular user can't add a trade for any customer """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for adding a trade for the created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Trade.objects.all().count() == 0


@pytest.mark.order(8)
@pytest.mark.django_db
def test_staff_cant_add_trade_for_deleted_vehicle():
    """ A staff member (or superuser) can't add a trade to a non-existent vehicle """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add trade for created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service,vehicle=created_vehicle)
    created_vehicle.delete()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Trade.objects.all().count() == 0


@pytest.mark.order(8)
@pytest.mark.django_db
def test_staff_cant_add_trade_for_deleted_service():
    """ A staff member (or superuser) can't add a trade to a non-existent service """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add trade for created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    created_service.delete()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 400
    assert Trade.objects.all().count() == 0


@pytest.mark.order(8)
@pytest.mark.django_db
def test_staff_cant_add_trade_if_not_authenticated():
    """ A staff member (or superuser) can't add trade if not authenticated """

    # create user, customer, service, vehicle, service
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_vehicle = random_vehicle(customer=created_customer)
    created_service = random_service()

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add trade for created customer
    url = reverse("trades")
    payload = random_trade_payload(service=created_service, vehicle=created_vehicle)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Trade.objects.all().count() == 0
