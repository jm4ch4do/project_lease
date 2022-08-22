import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_vehicle_payload, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Vehicle


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_get_vehicle_list():
    """ A staff member can get the list of all vehicles """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("vehicles")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['customer']
    assert response.data[0]['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_get_vehicle_list():
    """ A superuser can get the list of all customers """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_superuser = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for vehicle list
    url = reverse("vehicles")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['customer']
    assert response.data[0]['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_get_own_vehicle_details():
    """ A regular user can get his vehicle information """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("vehicle_edit", kwargs={'pk': created_vehicle.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['customer']
    assert response.data['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_gets_any_vehicles_details():
    """ A staff member can get any vehicle user data """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("vehicle_edit", kwargs={'pk': created_vehicle.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['customer']
    assert response.data['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_gets_any_vehicle_details():
    """ A superuser can get any vehicle user data """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create staff user
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for a vehicle
    url = reverse("vehicle_edit", kwargs={'pk': created_vehicle.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data['id'], int)
    assert response.data['customer']
    assert response.data['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_adds_own_vehicle():
    """ A regular user can add his own vehicle"""

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Vehicle.objects.all().count() == 1
    assert Vehicle.objects.first().model == payload['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_adds_any_vehicle():
    """ A staff member can add a vehicle to any customer """

    # create active customer
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

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Vehicle.objects.all().count() == 1
    assert Vehicle.objects.first().model == payload['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_superuser_adds_any_vehicle():
    """ A superuser can add a vehicle to any customer """

    # create active customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add vehicle for created customer
    url = reverse("vehicles")
    payload = random_vehicle_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert Vehicle.objects.all().count() == 1
    assert Vehicle.objects.first().model == payload['model']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_modify_own_vehicle_details():
    """ A regular user can modify his vehicle information"""

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("vehicle_edit", kwargs={'pk': created_vehicle.id})
    payload = random_vehicle_payload()
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("model")
    assert Vehicle.objects.first().model == payload["model"]


@pytest.mark.order(2)
@pytest.mark.django_db
def test_delete_own_vehicle_details():
    """ A regular user can delete his vehicle"""

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting vehicle
    url = reverse("vehicle_edit", kwargs={'pk': created_vehicle.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Vehicle.objects.all().count() == 0


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_can_search_vehicles():
    """ Staff user can search vehicles """

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # create user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # modify vehicle
    created_vehicle.make = 'aaaa'
    created_vehicle.model = 'bbbb'
    created_vehicle.year = 2020
    created_vehicle.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("vehicle_search")
    url += '?make=aaa&model=bbb&year=2020&'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert Vehicle.objects.first().model == created_vehicle.model
