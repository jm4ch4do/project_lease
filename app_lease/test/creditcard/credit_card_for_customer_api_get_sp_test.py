import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer, random_creditcard
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(7)
@pytest.mark.django_db
def test_user_cant_get_credit_cards_for_any_customer():
    """ A regular user can't get the credit cards for any customer """

    # create user, customer and credit_card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)
    created_credit_card2 = random_creditcard(customer=created_customer)

    # create regular user
    regular_user = random_user(is_active=True)

    # configure token for regular_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("credit_cards_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_non_auth_superuser_cant_get_credit_cards_for_any_customer():
    """ A superusercan't get the credit cards for a customer if not authenticated """

    # create user, customer and credit_card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)
    created_credit_card2 = random_creditcard(customer=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    # client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("credit_cards_for_customer", kwargs={'pk': created_customer.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 401
    assert response.data['response']


@pytest.mark.order(7)
@pytest.mark.django_db
def test_cant_get_credit_cards_of_non_existent_customer():
    """ When superuser tries to get credit cards of non-existent customer it will
        obtain a 404 error """

    # create user, customer and credit_card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)
    created_credit_card2 = random_creditcard(customer=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for superuser
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for all vehicle for the customer
    url = reverse("credit_cards_for_customer", kwargs={'pk': created_customer.id})
    created_customer.delete()
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 404
    assert response.data['response']
