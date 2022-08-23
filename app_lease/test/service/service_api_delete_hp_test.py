import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_service, random_user
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Service


@pytest.mark.order(6)
@pytest.mark.django_db
def test_staff_deletes_service():
    """ A staff user can delete any service """

    # create service
    created_service = random_service()

    # create staff_user
    staff_user = random_user(is_active=True)
    staff_user.is_staff = True
    staff_user.save()

    # configure token for staff_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=staff_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting service
    url = reverse("service_edit", kwargs={'pk': created_service.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Service.objects.all().count() == 0
