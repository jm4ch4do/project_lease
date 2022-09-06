import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_creditcard, random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_invalid_field_search_in_credit_card_list():
    """ Invalid field in the search results in 422 error """

    # create staff user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)
    created_credit_card.name_in_card = 'aaaa'
    created_credit_card.expire_year = 2020
    created_credit_card.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("credit_card_search")
    url += '?email=bbb'
    response = client.get(url)

    # get data back
    assert response.status_code == 422
    assert len(response.data) == 1
    assert response.data['response']


@pytest.mark.order(2)
@pytest.mark.django_db
def test_regular_user_cant_search_credit_cards():
    """ Regular users can't perform credit card searches """

    # create regular user
    regular_user = random_user(is_active=True)

    # create user, customer and credit card
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_credit_card = random_creditcard(customer=created_customer)
    created_credit_card.name_in_card = 'aaaa'
    created_credit_card.expire_year = 2020
    created_credit_card.save()

    # configure token for regular user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=regular_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("credit_card_search")
    url += '?name_in_card=aaa&expire_year=2020'
    response = client.get(url)

    # get data back
    assert response.status_code == 401
    assert response.data['response']
