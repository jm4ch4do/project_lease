# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Lead
from app_lease.test.generator import random_lead
from django.contrib.auth.models import User


@pytest.mark.order(4)
@pytest.mark.django_db
def test_create_lead():
    """ Test lead creation which doesn't affect any other table """

    created_lead = random_lead()
    assert True if isinstance(created_lead, Lead) else False  # Lead object created
    assert True if Lead.objects.all().count() == 1 else False  # only one object in table lead


@pytest.mark.order(4)
@pytest.mark.django_db
def test_delete_lead():
    """ Basic test for deleting lead """

    created_lead = random_lead()
    # deleting lead should clear lead table
    Lead.objects.all().delete()
    assert True if Lead.objects.all().count() == 0 else False


@pytest.mark.order(4)
@pytest.mark.django_db
def test_custom_lead():
    """ Testing custom methods in lead """

    created_lead = random_lead()
    assert True if isinstance(str(random_lead), str) else False  # object returns valid string
    assert True if isinstance(created_lead.age, int) else False  # age return valid int
