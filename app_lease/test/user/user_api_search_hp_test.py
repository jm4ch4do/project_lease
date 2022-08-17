import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user, random_customer
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_staff_and_superuser_can_search():
    """ Staff and Superusers can both search users by:
        username, first_name and last_name """

    # create user
    created_user = random_user(is_active=1)
    created_user.username = "aaaa"
    created_user.first_name = "bbbb"
    created_user.last_name = "cccc"
    created_user.save()

    # create staff_user
    staff_user = random_user(is_active=1)
    staff_user.username = "dddd"
    staff_user.first_name = "dddd"
    staff_user.last_name = "dddd"
    staff_user.is_staff = True
    staff_user.save()

    # create super_user
    super_user = random_user(is_active=1)
    super_user.username = "eeee"
    super_user.first_name = "eeee"
    super_user.last_name = "eeee"
    super_user.is_staff = True
    super_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?username=aaa' + '&first_name=bbb' + '&last_name=ccc'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert isinstance(response.data[0]['username'], str)
    assert isinstance(response.data[0]['customer_id'], int)
    assert not response.data[0].get('password')
    assert not response.data[0].get('token')

    # configure token for super_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=super_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request
    url = reverse("user_search")
    url += '?username=aaa' + '&first_name=bbb' + '&last_name=ccc'
    response = client.get(url)

    # get data back
    assert response.status_code == 200
    assert len(response.data) == 1
    assert isinstance(response.data[0]['username'], str)
    assert isinstance(response.data[0]['customer_id'], int)
    assert not response.data[0].get('password')
    assert not response.data[0].get('token')
