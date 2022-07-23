from faker import Faker
from app_lease.test.generator import Provider, random_customer
from app_lease.models import Vehicle
from faker_vehicle import VehicleProvider


def random_vehicle(total=1, customer=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)
    fake.add_provider(VehicleProvider)

    # ----- create vehicles
    created_vehicles = []
    for _ in range(total):

        # create customer if needed
        created_customer = random_customer() if not customer else customer

        # create  vehicle
        created_vehicle = Vehicle.objects.create(
            customer=created_customer,
            make_model=fake.vehicle_make_model(),
            make=fake.vehicle_make(),
            model=fake.vehicle_model(),
            category=fake.vehicle_category(),
            machine_make_model=fake.machine_make_model(),
            machine_make=fake.machine_make(),
            machine_model=fake.machine_model(),
            machine_category=fake.machine_category(),
            year=fake.vehicle_year(),
            machine_year=fake.machine_year()
        )

        created_vehicles.append(created_vehicle)

    if len(created_vehicles) == 1:
        return created_vehicle
    else:
        return created_vehicles
