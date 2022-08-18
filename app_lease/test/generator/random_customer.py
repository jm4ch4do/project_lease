from faker import Faker
from app_lease.test.generator.random_user import random_user
from app_lease.utils.fake_provider import Provider
from app_lease.models import Customer
from datetime import datetime


def random_customer(total=1, user=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create customers
    created_customers = []
    for _ in range(total):

        # create user if needed
        created_user = random_user() if not user else user

        # create customer
        created_customer = Customer.objects.create(
            user=created_user,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            job=fake.job(),
            notes=fake.paragraph(nb_sentences=3),
            dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
            status=Provider.get_customer_status(created_user)  # status matches the user status
        )

        created_customers.append(created_customer)

    if len(created_customers) == 1:
        return created_customer
    else:
        return created_customers


def random_customer_payload(user=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # random first_name and last_name
    random_first_name = fake.first_name()
    random_last_name = fake.last_name()
    random_user_name = Provider.get_random_user_name(random_first_name)

    # create random user payload
    payload = dict(
        first_name=random_first_name,
        last_name=random_last_name,
        job=fake.job(),
        status=1,
        notes=fake.paragraph(nb_sentences=3),
        dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
    )

    if user is not None:
        payload['user'] = user

    return payload
