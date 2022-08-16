from faker import Faker
from app_lease.utils.fake_provider import Provider
from django.contrib.auth.models import User
from random import getrandbits
from datetime import datetime


def random_user(total=1, is_active=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create users
    created_users = []
    for _ in range(total):

        # random first_name and last_name
        random_first_name = fake.first_name()
        random_last_name = fake.last_name()
        random_user_name = Provider.get_random_user_name(random_first_name)
        is_active = bool(getrandbits(1)) if not is_active else is_active

        created_user = User(
            is_superuser=False,
            first_name=random_first_name,
            last_name=random_last_name,
            username=random_user_name,
            email=random_user_name + "@gmail.com",
            is_active=is_active
        )

        created_user.set_password("Teclado123*")
        created_user.save()


        created_users.append(created_user)

    if len(created_users) == 1:
        return created_user
    else:
        return created_users


def random_user_customer_payload():

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # random first_name and last_name
    random_first_name = fake.first_name()
    random_last_name = fake.last_name()
    random_user_name = Provider.get_random_user_name(random_first_name)

    # create random user payload
    payload = dict(
        password="Teclado123*",
        password2="Teclado123*",
        is_superuser=False,
        first_name=random_first_name,
        last_name=random_last_name,
        username=random_user_name,
        email=random_user_name + "@gmail.com",
        is_active=1,
        job=fake.job(),
        notes=fake.paragraph(nb_sentences=3),
        dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
    )
    return payload
