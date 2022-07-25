import pytest
from faker import Faker
from datetime import datetime
from app_lease.models import Customer, Lead
from django.contrib.auth.models import User
from app_lease.utils.lead_to_customer import lead_to_customer
from app_lease.test.generator import random_lead

@pytest.mark.django_db
def test_utils_lead_to_customer():

    """ Testing function lead_to_customer from the utils folder """
    created_lead = random_lead()
    created_customer = lead_to_customer(created_lead)
    assert True if isinstance(created_customer, Customer) else False  # customer instance created
    assert True if Customer.objects.all().count() == 1 else False  # customer created
    assert True if User.objects.all().count() == 1 else False  # user created
    assert True if Lead.objects.all().count() == 0 else False  # lead deleted


