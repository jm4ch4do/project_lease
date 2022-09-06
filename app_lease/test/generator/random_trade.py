from faker import Faker
from app_lease.test.generator.random_vehicle import random_vehicle
from app_lease.test.generator.random_service import random_service
from app_lease.utils.fake_provider import Provider
from app_lease.models import Trade
from django.core.exceptions import ValidationError


def random_trade(total=1, service=None, vehicle=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # can't create multiple trades for same service, vehicle combination
    if total > 1 and service and vehicle:
        raise ValidationError(
            "You can only have one trade per service/vehicle combination",
            code='trade_per_customer_service_vehicle'
        )

    else:

        # ----- create trades
        created_trades = []
        for _ in range(total):

            # create vehicle if needed
            created_vehicle = vehicle if vehicle else random_vehicle()

            # create service if needed
            created_service = service if service else random_service()

            # create trade
            created_trade = Trade.objects.create(
                service=created_service,
                vehicle=created_vehicle,
                note=fake.paragraph(nb_sentences=3),
            )

            created_trades.append(created_trade)

        if len(created_trades) == 1:
            return created_trade
        else:
            return created_trades

def random_trade_payload(service, vehicle):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # create random trade payload
    payload = dict(
        service=service.id,
        vehicle=vehicle.id,
        note=fake.paragraph(nb_sentences=3),
    )

    return payload
