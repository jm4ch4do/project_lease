# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Service
from app_lease.test.generator import random_service
from django.contrib.auth.models import User


@pytest.mark.order(6)
@pytest.mark.django_db
def test_create_service():
    """ Test lead creation which doesn't affect any other table """

    created_service = random_service()
    assert True if isinstance(created_service, Service) else False  # Service object created
    assert True if Service.objects.all().count() == 1 else False  # only one object in table service


@pytest.mark.order(6)
@pytest.mark.django_db
def test_delete_service():
    """ Basic test for deleting service """

    created_lead = random_service()
    Service.objects.all().delete()
    assert True if Service.objects.all().count() == 0 else False


@pytest.mark.order(6)
@pytest.mark.django_db
def test_custom_service():
    """ Testing custom methods in service """

    created_service = random_service()
    assert True if isinstance(str(random_service), str) else False  # object returns valid string
    assert True if isinstance(created_service.label, str) else False  # label return valid int
