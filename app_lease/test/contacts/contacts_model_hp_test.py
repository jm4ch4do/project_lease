# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Contact, Customer, Lead
from app_lease.test.generator import random_contact
from django.contrib.auth.models import User

@pytest.mark.order(5)
@pytest.mark.django_db
def test_create_contact_with_email_for_customer():

    created_contact = random_contact()
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if Contact.objects.all().count() == 1 else False  # only one object in table contact
    assert True if Customer.objects.all().count() == 1 else False  # only one object in table customer
    assert True if isinstance(created_contact.customer, Customer) else False  # contact has valid customer
    assert True if not created_contact.lead else False  # contact has no lead
    assert True if created_contact.email else False  # contact has an email
    assert True if not created_contact.phone else False  # contact has no phone
    assert True if created_contact.type == 1 else False  # contact has type 1 (email)\


@pytest.mark.order(5)
@pytest.mark.django_db
def test_create_contact_with_phone_for_customer():

    created_contact = random_contact(contact_type=2)
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if Contact.objects.all().count() == 1 else False  # only two objects in table contact
    assert True if Customer.objects.all().count() == 1 else False  # only two objects in table customer
    assert True if isinstance(created_contact.customer, Customer) else False  # contact has valid customer
    assert True if not created_contact.lead else False  # contact has no lead
    assert True if created_contact.phone else False  # contact has a phone
    assert True if not created_contact.email else False  # contact has no email
    assert True if created_contact.type == 2 else False  # contact has type 2 (phone)


@pytest.mark.order(5)
@pytest.mark.django_db
def test_create_contact_with_email_for_lead():

    created_contact = random_contact(related_to='lead')
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if isinstance(created_contact.lead, Lead) else False  # contact has valid lead
    assert True if not created_contact.customer else False  # contact has no customer
    assert True if created_contact.email else False  # contact has an email
    assert True if not created_contact.phone else False  # contact has no phone
    assert True if created_contact.type == 1 else False  # contact has type 1 (email)


@pytest.mark.order(5)
@pytest.mark.django_db
def test_create_contact_with_phone_for_lead():
    # create contact with phone for a lead
    created_contact = random_contact(related_to='lead', contact_type=2)
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if isinstance(created_contact.lead, Lead) else False  # contact has valid lead
    assert True if not created_contact.customer else False  # contact has no customer
    assert True if created_contact.phone else False  # contact has a phone
    assert True if not created_contact.email else False  # contact has no email
    assert True if created_contact.type == 2 else False  # contact has type 2 (phone)


@pytest.mark.order(5)
@pytest.mark.django_db
def test_delete_contact_dont_delete_related_customer():

    created_contact = random_contact()  # also creates a related customer and user
    created_contact.delete()
    assert True if Customer.objects.all().count() == 1 else False  # customer was not removed
    assert True if User.objects.all().count() == 1 else False  # user was not removed


@pytest.mark.order(5)
@pytest.mark.django_db
def test_delete_contact_dont_delete_related_lead():

    created_contact = random_contact(related_to='lead')  # also creates a related customer and user
    created_contact.delete()
    assert True if Lead.objects.all().count() == 1 else False  # lead was not removed


@pytest.mark.order(5)
@pytest.mark.django_db
def test_delete_customer_delete_contact():

    created_contact = random_contact()
    related_customer = created_contact.customer
    related_customer.delete()
    assert True if Contact.objects.all().count() == 0 else False  # customer was not removed


@pytest.mark.order(5)
@pytest.mark.django_db
def test_custom_contact():
    # testing custom methods in customer
    created_contact = random_contact()
    assert True if isinstance(str(random_contact), str) else False  # object returns valid string




# sp
# create contact without customer or lead
# create contact without phone or email
# put letter in the phone
# put too much or too little numbers in the phone
# put false email in emails