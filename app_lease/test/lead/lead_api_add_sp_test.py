import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Lead
from app_lease.test.generator import random_lead_payload


@pytest.mark.order(2)
@pytest.mark.django_db
def test_user_cant_add_any_lead():
    """ Lead creation is not available to regular users """

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for add lead
    url = reverse("leads")
    payload = random_lead_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert Lead.objects.all().count() == 0


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_cant_add_lead_if_not_authenticated():
    """ A staff member (or superuser) can't add lead if not authenticated """

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

    # make request to add new lead
    url = reverse("leads")
    payload = random_lead_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('response')
    assert Lead.objects.all().count() == 0


@pytest.mark.order(2)
@pytest.mark.django_db
def test_inactive_staff_cant_add_lead():
    """ An inactive staff member (or superuser) can't add lead """

    # create staff member
    staff_user = random_user()
    staff_user.is_staff = True
    staff_user.is_active = False
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new lead
    url = reverse("leads")
    payload = random_lead_payload()
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 401
    assert response.data.get('detail')
    assert Lead.objects.all().count() == 0
