# ------------------------------ TEST FUNCTION FROM UTILS ------------------------------
# import pytest
# from app_lease.models import Customer
# from app_lease.test.generator import random_lead
# from django.contrib.auth.models import User
#
#
# @pytest.mark.django_db
# def test_lead_to_customer():
#
#     # create lead with contacts
#     created_lead = random_lead()
#
#     # turn it into customer
#
#
#     created_customer = random_customer()
#     assert True if isinstance(created_customer, Customer) else False  # Customer object created
#     assert True if Customer.objects.all().count() == 1 else False  # only one object in table customers
#     assert True if Customer.objects.all().count() == 1 else False  # only one object in table users
#     assert True if Customer.objects.first().user.id == User.objects.first().id else False  # user and customer relation
