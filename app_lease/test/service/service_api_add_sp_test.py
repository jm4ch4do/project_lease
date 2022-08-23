import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Service
from app_lease.test.generator import random_service_payload


@pytest.mark.order(6)
@pytest.mark.django_db
def test_user_cant_add_service():
    """ Service creation is not available to regular users """

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add lead
    url = reverse("services")
    payload = random_service_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Service.objects.all().count() == 0


@pytest.mark.order(6)
@pytest.mark.django_db
def test_staff_cant_add_service_if_not_authenticated():
    """ A staff member (or superuser) can't add service if not authenticated """

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new service
    url = reverse("services")
    payload = random_service_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Service.objects.all().count() == 0


@pytest.mark.order(6)
@pytest.mark.django_db
def test_inactive_staff_cant_add_service():
    """ An inactive staff member (or superuser) can't add service """

    # create inactive staff member
    staff_user = random_user()
    staff_user.is_staff = True
    staff_user.is_active = False
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new lead
    url = reverse("services")
    payload = random_service_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('detail')
    assert Service.objects.all().count() == 0
