# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Contact, Customer, Lead
from app_lease.test.generator import random_contact
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_contact():

    # create contact with email for a customer
    created_contact = random_contact()
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if Contact.objects.all().count() == 1 else False  # only one object in table contact
    assert True if Customer.objects.all().count() == 1 else False  # only one object in table customer
    assert True if isinstance(created_contact.customer, Customer) else False  # contact has valid customer
    assert True if not created_contact.lead else False  # contact has no lead
    assert True if created_contact.email else False  # contact has an email
    assert True if not created_contact.phone else False  # contact has no phone
    assert True if created_contact.type == 1 else False # contact has type 1 (email)

    # create contact with phone for a customer
    created_contact = random_contact(contact_type=2)
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if Contact.objects.all().count() == 2 else False  # only two objects in table contact
    assert True if Customer.objects.all().count() == 2 else False  # only two objects in table customer
    assert True if isinstance(created_contact.customer, Customer) else False  # contact has valid customer
    assert True if not created_contact.lead else False  # contact has no lead
    assert True if created_contact.phone else False  # contact has a phone
    assert True if not created_contact.email else False  # contact has no email
    assert True if created_contact.type == 2 else False  # contact has type 2 (phone)

    # create contact with email for a lead
    created_contact = random_contact(related_to='lead')
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if isinstance(created_contact.lead, Lead) else False  # contact has valid lead
    assert True if not created_contact.customer else False  # contact has no customer
    assert True if created_contact.email else False  # contact has an email
    assert True if not created_contact.phone else False  # contact has no phone
    assert True if created_contact.type == 1 else False # contact has type 1 (email)

    # create contact with phone for a lead
    created_contact = random_contact(related_to='lead', contact_type=2)
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if isinstance(created_contact.lead, Lead) else False  # contact has valid lead
    assert True if not created_contact.customer else False  # contact has no customer
    assert True if created_contact.phone else False  # contact has a phone
    assert True if not created_contact.email else False  # contact has no email
    assert True if created_contact.type == 2 else False  # contact has type 2 (phone)


# create contact
# contact delete should not delete customer or lead
# customer delete should delete contact
# lead delete should delete contact
# contact string output


# sp
# create contact without customer or lead
# create contact without phone or email
# put letter in the phone
# put too much or too little numbers in the phone
# put false email in emails



# @pytest.mark.django_db
# def test_delete_lead():
#     created_lead = random_lead()
#     # deleting lead should clear lead table
#     Lead.objects.all().delete()
#     assert True if Lead.objects.all().count() == 0 else False
#
#
# @pytest.mark.django_db
# def test_custom_lead():
#     # testing custom methods in customer
#     created_lead = random_lead()
#     assert True if isinstance(str(random_lead), str) else False  # object returns valid string
#     assert True if isinstance(created_lead.age, int) else False  # age return valid int
