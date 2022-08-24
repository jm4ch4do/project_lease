from faker import Faker
from app_lease.test.generator.random_user import random_user
from app_lease.test.generator.random_customer import random_customer
from app_lease.utils.fake_provider import Provider
from app_lease.models import CreditCard
from datetime import datetime
from random import randint


def random_creditcard(total=1, customer=None, name_in_card=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create credit cards
    created_creditcards = []
    for _ in range(total):

        # create customer if needed
        created_customer = random_customer() if not customer else customer
        created_name_in_card = created_customer.first_name + created_customer.last_name \
            if not name_in_card else name_in_card

        # create creditcard
        created_creditcard = CreditCard.objects.create(
            customer=created_customer,
            name_in_card=created_name_in_card,
            provider=fake.credit_card_provider(),
            expire_month=randint(1, 12),
            expire_year=randint(datetime.today().year, datetime.today().year + 5),
            security_code=fake.credit_card_security_code(),
            card_number=fake.credit_card_number(),
        )

        created_creditcards.append(created_creditcard)

    if len(created_creditcards) == 1:
        return created_creditcard
    else:
        return created_creditcards


def random_creditcard_payload(customer):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # create random user payload
    payload = dict(
        customer=customer.id,
        name_in_card=customer.first_name + customer.last_name,
        provider=fake.credit_card_provider(),
        expire_month=randint(1, 12),
        expire_year=randint(datetime.today().year, datetime.today().year + 5),
        security_code=fake.credit_card_security_code(),
        card_number=fake.credit_card_number(),
    )

    return payload
