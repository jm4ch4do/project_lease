import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Customer


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
