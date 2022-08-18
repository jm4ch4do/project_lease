import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_user_payload, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.order(2)
@pytest.mark.django_db
def test_get_own_user():
    """ A regular user can get his own user data """

    # create user
    created_user = random_user(is_active=1)

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for getting user details
    url = reverse("user_edit", kwargs={'pk': created_user.id})
    response = client.get(url)

    # response has the correct values
    assert response.status_code == 200
    assert response.data.get("email")
    assert response.data.get("username")
    assert response.data.get("is_active") is not None
    assert response.data.get("is_staff") is not None
    assert response.data.get("customer_id") is not None
    assert response.data.get('id')
    assert "password" not in response.data





# can get own user
# can get user as staff member
# can get user as superuser

# can't get user if not authenticate
# can't get user if user doesn't exist
# can't get user if not own user

# staff user can't edit another staff user, only regular users
# superuser can edit staff users and other superusers
