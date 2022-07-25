# ------------------------------ CUSTOMER MODEL SAD PATH ------------------------------
import pytest
from app_lease.models import Contact, Customer, Lead
from app_lease.test.generator import random_contact, random_lead
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from faker import Faker


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_need_related_customer():
    """ A contact does not allow deleting its related customer """
    created_contact = random_contact()
    with pytest.raises(ValidationError) as exp:
        created_contact.customer = None
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_customer_need_related_lead():
    """ A contact does not allow deleting its related lead """
    created_contact = random_contact(related_to='lead')
    with pytest.raises(ValidationError) as exp:
        created_contact.lead = None
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_cant_have_related_customer_and_lead():
    """ A contact can't have both a related customer and a related lead """
    created_contact = random_contact()
    created_lead = random_lead()

    with pytest.raises(ValidationError) as exp:
        created_contact.lead = created_lead
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_need_related_email():
    """ A contact doesn't allow deleting its email """

    created_contact = random_contact()
    with pytest.raises(ValidationError) as exp:
        created_contact.email = None
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_need_related_phone():
    """ A contact doesn't allow deleting its phone """

    created_contact = random_contact(contact_type=2)
    with pytest.raises(ValidationError) as exp:
        created_contact.phone = None
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_cant_have_related_phone_and_email():
    """ A contact doesn't allow having both email and phone """
    fake = Faker()
    created_contact = random_contact()
    random_phone = int("1" + str(fake.msisdn()[3:]))

    with pytest.raises(ValidationError) as exp:
        created_contact.phone = random_phone
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_bad_phone():
    """ Phone input must be validated"""

    fake = Faker()
    created_contact = random_contact(contact_type=2)
    random_phone = "1" + str(fake.msisdn()[3:])
    random_phone = int(random_phone[4:])

    with pytest.raises(ValidationError) as exp:
        created_contact.phone = random_phone
        created_contact.full_clean()
    assert True if exp else False


@pytest.mark.order(5)
@pytest.mark.django_db
def test_contact_bad_phone():
    """ Email input must be validated """

    created_contact = random_contact()

    random_email_no_at_sign = 'testing.com'
    with pytest.raises(ValidationError) as exp:
        created_contact.email = random_email_no_at_sign
        created_contact.full_clean()
    assert True if exp else False

    random_email_no_dot = 'testing@testingcom'
    with pytest.raises(ValidationError) as exp:
        created_contact.email = random_email_no_dot
        created_contact.full_clean()
    assert True if exp else False
