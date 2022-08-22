import pytest
from rest_framework.test import APIClient
from app_lease.test.generator import random_customer, random_user, random_vehicle_payload, random_vehicle
from django.urls import reverse
from rest_framework.authtoken.models import Token
from app_lease.models import Vehicle


@pytest.mark.order(2)
@pytest.mark.django_db
def test_delete_own_vehicle_details():
    """ A regular user can delete his vehicle"""

    # create vehicle with active customer and user
    created_vehicle = random_vehicle()
    created_customer = created_vehicle.customer
    created_customer.status = 1
    created_customer.save()
    created_user = created_customer.user
    created_user.is_active = True
    created_user.save()

    # configure token for created_user
    client = APIClient()
    token, created = Token.objects.get_or_create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    # make request for deleting vehicle
    url = reverse("vehicle_edit", kwargs={'pk': created_vehicle.id})
    response = client.delete(url)

    # response has the correct values
    assert response.status_code == 204
    assert response.data.get("response")
    assert Vehicle.objects.all().count() == 0
