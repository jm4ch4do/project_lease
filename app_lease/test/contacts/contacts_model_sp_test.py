# ------------------------------ CUSTOMER MODEL SAD PATH ------------------------------
import pytest
from app_lease.models import Contact, Customer, Lead
from app_lease.test.generator import random_contact, random_lead
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError


@pytest.mark.django_db
def test_customer_need_related_customer():

    created_contact = random_contact()
    with pytest.raises(ValidationError) as exp:
        created_contact.customer = None
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.django_db
def test_customer_need_related_lead():

    created_contact = random_contact(related_to='lead')
    with pytest.raises(ValidationError) as exp:
        created_contact.lead = None
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.django_db
def test_customer_cant_have_related_contact_and_lead():

    created_contact = random_contact()
    created_lead = random_lead()

    with pytest.raises(ValidationError) as exp:
        created_contact.lead = created_lead
        created_contact.full_clean()
    assert True if exp else False


# sp
# create contact without customer or lead
# create contact without phone or email
# put letter in the phone
# put too much or too little numbers in the phone
# put false email in emails