import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_contact, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(5)
@pytest.mark.django_db
def test_staff_can_search_contacts():
    """ Staff user can search contacts """

    # create user, customer and contact
    created_user = random_user(is_active=True)
    created_customer = random_customer(user=created_user)
    created_contact = random_contact(owner=created_customer)

    # create staff member
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # modify contact
    created_contact.note = 'aaaa'
    created_contact.type = 1
    created_contact.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("contact_search")
    url += '?note=aaa&type=1'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get('note') == created_contact.note
