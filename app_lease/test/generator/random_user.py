from faker import Faker
from app_lease.utils.fake_provider import Provider
from django.contrib.auth.models import User
from random import getrandbits


def random_user(total=1):

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

        created_user = User.objects.create(
            password="Teclado123",
            is_superuser=False,
            first_name=random_first_name,
            last_name=random_last_name,
            username=random_user_name,
            email=random_user_name + "@gmail.com",
            is_active=bool(getrandbits(1))
        )

        created_users.append(created_user)

    if len(created_users) == 1:
        return created_user
    else:
        return created_users


def random_user_payload():

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # random first_name and last_name
    random_first_name = fake.first_name()
    random_last_name = fake.last_name()
    random_user_name = Provider.get_random_user_name(random_first_name)

    # create random user payload
    payload = dict(
        password="Teclado123",
        is_superuser=False,
        first_name=random_first_name,
        last_name=random_last_name,
        username=random_user_name,
        email=random_user_name + "@gmail.com",
        is_active=bool(getrandbits(1))
    )
    return payload
