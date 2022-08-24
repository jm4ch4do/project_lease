import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_creditcard
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(11)
@pytest.mark.django_db
def test_get_own_credit_card_details():
    """ A regular user can get his own credit card details """

    # create user, customer and credit_card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("name_in_card")
    assert response.data.get("provider")


@pytest.mark.order(11)
@pytest.mark.django_db
def test_staff_gets_any_credit_card_details():
    """ A staff member can get any credit card details """

    # create user, customer and credit_card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("name_in_card")
    assert response.data.get("provider")


@pytest.mark.order(11)
@pytest.mark.django_db
def test_superuser_gets_any_credit_card_details():
    """ A superuser can get any credit card details """

    # create user, customer and credit_card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # create superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting customer details
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("id")
    assert response.data.get("name_in_card")
    assert response.data.get("provider")
