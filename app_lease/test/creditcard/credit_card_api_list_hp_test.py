import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_creditcard
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(11)
@pytest.mark.django_db
def test_staff_get_credit_card_list():
    """ A staff member can get the list of all credit cards """

    # create staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # create user, customer and creditcard
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for credit card list
    url = reverse("credit_cards")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['name_in_card']
    assert response.data[0]['provider']


@pytest.mark.order(11)
@pytest.mark.django_db
def test_superuser_get_credit_card_list():
    """ A superuser can get the list of all credit cards """

    # create superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = True
    super_user.save()

    # create user, customer and creditcard
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for credit card list
    url = reverse("credit_cards")
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert isinstance(response.data[0]['id'], int)
    assert response.data[0]['name_in_card']
    assert response.data[0]['provider']
