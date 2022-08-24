import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_creditcard, random_creditcard_payload
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import CreditCard


@pytest.mark.order(11)
@pytest.mark.django_db
def test_modify_own_credit_card_details():
    """ A regular user can modify his own credit card information"""

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting credit card details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    payload = random_creditcard_payload(customer=created_customer)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("provider")
    assert CreditCard.objects.first().name_in_card == payload["name_in_card"]


@pytest.mark.order(11)
@pytest.mark.django_db
def test_staff_modify_any_credit_card_details():
    """ A staff member can modify his own credit card information"""

    # created staff member
    staff_user = random_user(is_active=1)
    staff_user.is_staff = True
    staff_user.save()

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting credit card details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    payload = random_creditcard_payload(customer=created_customer)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("provider")
    assert CreditCard.objects.first().name_in_card == payload["name_in_card"]


@pytest.mark.order(11)
@pytest.mark.django_db
def test_superuser_modify_any_credit_card_details():
    """ A superuser can modify his own credit card information"""

    # created superuser
    super_user = random_user(is_active=1)
    super_user.is_superuser = True
    super_user.save()

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting credit card details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    payload = random_creditcard_payload(customer=created_customer)
    response = client.put(url, payload)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("provider")
    assert CreditCard.objects.first().name_in_card == payload["name_in_card"]
