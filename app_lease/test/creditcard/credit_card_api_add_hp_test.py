import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_creditcard_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import CreditCard


@pytest.mark.order(11)
@pytest.mark.django_db
def test_user_adds_own_credit_card():
    """ A regular user can add a credit card for himself """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # configure token for user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new credit card
    url = reverse("credit_cards")
    payload = random_creditcard_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert CreditCard.objects.all().count() == 1
    assert CreditCard.objects.first().name_in_card == payload['name_in_card']
    assert CreditCard.objects.first().customer == created_customer


@pytest.mark.order(11)
@pytest.mark.django_db
def test_staff_adds_credit_card():
    """ A staff member can add a credit card for any user """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new credit card
    url = reverse("credit_cards")
    payload = random_creditcard_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert CreditCard.objects.all().count() == 1
    assert CreditCard.objects.first().name_in_card == payload['name_in_card']
    assert CreditCard.objects.first().customer == created_customer


@pytest.mark.order(11)
@pytest.mark.django_db
def test_superuser_adds_credit_card():
    """ A superuser can add a credit card for any user """

    # create user and customer
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)

    # create staff member
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff member
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request to add new credit card
    url = reverse("credit_cards")
    payload = random_creditcard_payload(customer=created_customer)
    response = client.post(url, payload)

    # response has the correct values
    assert response.status_code == 201
    assert CreditCard.objects.all().count() == 1
    assert CreditCard.objects.first().name_in_card == payload['name_in_card']
    assert CreditCard.objects.first().customer == created_customer
