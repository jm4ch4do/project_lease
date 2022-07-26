from faker import Faker
from app_lease.test.generator.random_user import Provider
from app_lease.models import Service
from random import randint, random


def random_service(total=1):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create services
    created_services = []
    for _ in range(total):

        # create service
        created_service = Service.objects.create(
            name=fake.sentence(nb_words=2),
            cost=round(random() * 1000, 2),
            when_to_pay=randint(1, 2),
            service_type=randint(1, 2),
            description=fake.paragraph(nb_sentences=3),
        )

        created_services.append(created_service)

    if len(created_services) == 1:
        return created_service
    else:
        return created_services
