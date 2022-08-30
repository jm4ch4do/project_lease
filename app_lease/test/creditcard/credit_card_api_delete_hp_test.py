import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_creditcard, random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import CreditCard


@pytest.mark.order(11)
@pytest.mark.django_db
def test_user_deletes_own_credit_card():
    """ A regular user can delete his own credit card"""

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # configure token for user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting credit card
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert CreditCard.objects.all().count() == 0


@pytest.mark.order(11)
@pytest.mark.django_db
def test_staff_deletes_any_credit_card():
    """ A staff member can delete any credit card"""

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # created staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting credit card
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert CreditCard.objects.all().count() == 0


@pytest.mark.order(11)
@pytest.mark.django_db
def test_superuser_deletes_any_credit_card():
    """ A superuser can delete any credit card"""

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)

    # created superuser
    super_user = random_user(is_active=True)
    super_user.is_superuser = True
    super_user.save()

    # configure token for user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting credit card
    url = reverse("credit_card_edit", kwargs={'pk': created_credit_card.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert CreditCard.objects.all().count() == 0
