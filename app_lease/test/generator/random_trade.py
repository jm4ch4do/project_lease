from faker import Faker
from app_lease.test.generator.random_customer import random_customer
from app_lease.test.generator.random_vehicle import random_vehicle
from app_lease.test.generator.random_service import random_service
from app_lease.utils.fake_provider import Provider
from app_lease.models import Trade
from django.core.exceptions import ValidationError
from random import randint


def random_trade(total=1, customer=None, service=None, vehicle=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # can't create multiple trades for same customer, service, vehicle combination
    if total > 1 and customer and service and vehicle:
        raise ValidationError(
            "You can only have one trade per customer/service/vehicle combination",
            code='trade_per_customer_service_vehicle'
        )

    else:

        # ----- create trades
        created_trades = []
        for _ in range(total):

            # create customer if needed
            created_customer = customer if customer else random_customer()

            # create vehicle if needed
            created_vehicle = vehicle if vehicle else random_vehicle(customer=created_customer)

            # create service if needed
            created_service = service if service else random_service()

            # create trade
            created_trade = Trade.objects.create(
                customer=created_customer,
                service=created_service,
                vehicle=created_vehicle,
                note=fake.paragraph(nb_sentences=3),
                status=randint(1, 3)
            )

            created_trades.append(created_trade)

        if len(created_trades) == 1:
            return created_trade
        else:
            return created_trades
