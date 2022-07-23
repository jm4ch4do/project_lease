from faker import Faker
from random import randint
from app_lease.models import Customer, Contact
from django.contrib.auth.models import User
from app_lease.utils.fake_provider import Provider
from datetime import datetime


def lead_to_customer(lead, username=None, password=None):
    """
    Turns a lead into a customer and saves in the db. Returns the new customer object
    (lead_object, string, string) -> customer_object
    """

    # no username provided, create one which is not in the database
    if not username:
        while 1:
            username = lead.first_name.lower() + str(randint(1, 999999))
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                break

    if not password:
        password = 'Teclado123'

    # create user
    created_user = User.objects.create(
        password=password,
        is_superuser=False,
        first_name=lead.first_name,
        last_name=lead.last_name,
        username=username,
        email=username + "@gmail.com",
        is_active=1
    )

    # create_customer
    fake = Faker()
    created_customer = Customer.objects.create(
        user=created_user,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        job=fake.job(),
        notes=fake.paragraph(nb_sentences=3),
        dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
        status=Provider.get_customer_status(created_user)  # status matches the user status
    )

    # find contacts belonging to lead
    available_contacts = Contact.objects.filter(lead=lead)

    # move contacts from lead to customer if any
    if available_contacts:
        for contact in available_contacts:
            contact.lead = None
            contact.customer = created_customer

    # delete lead
    lead.delete()
