# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Contact
from app_lease.test.generator import random_contact
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_contact():
    created_contact = random_contact()
    assert True if isinstance(created_contact, Contact) else False  # Contact object created
    assert True if Contact.objects.all().count() == 1 else False  # only one object in table contact



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
