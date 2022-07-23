from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from app_lease.models import Customer, Contact, Lead, Vehicle, Service
from django.contrib.auth.models import User
from datetime import datetime
from random import getrandbits
from app_lease.utils.fake_provider import Provider


class Command(BaseCommand):

    help = "Creates Users, Customers, Leads and Contacts"

    def add_arguments(self, parser):

        # positional argument (mandatory argument) [python manage.py create_data 10]
        # parser.add_argument('total', type=int, help='Number of users to be created')

        # optional argument
        parser.add_argument('-t', '--total', type=str, help='Number of users to be created')

    def handle(self, *args, **kwargs):

        # constants
        DEFAULT_TOTAL_USERS = 100

        # arguments
        total = kwargs['total']
        total_users = DEFAULT_TOTAL_USERS if not total else int(total)
        total_leads = total_users * 2  # always create more leads than users
        total_vehicles = int(total_users / 2)  # half of users will have vehicles

        # register custom functions
        fake = Faker()
        fake.add_provider(Provider)
        fake.add_provider(VehicleProvider)

        # delete user, customers, leads, services, vehicles, contacts
        User.objects.all().delete()
        Customer.objects.all().delete()
        Lead.objects.all().delete()
        Service.objects.all().delete()
        Vehicle.objects.all().delete()
        Contact.objects.all().delete()

        # ----- generate users
        for _ in range(total_users):

            # random first_name and last_name
            random_first_name = fake.first_name()
            random_last_name = fake.last_name()
            random_user_name = Provider.get_random_user_name(random_first_name)

            User.objects.create(
                password="Teclado123",
                is_superuser=False,
                first_name=random_first_name,
                last_name=random_last_name,
                username=random_user_name,
                email=random_user_name + "@gmail.com",
                is_active=bool(getrandbits(1))
            )

        # ----- create one customer per user
        for _ in range(total_users):

            # use any username with no repetition
            random_user = fake.unique.get_random_user()

            # use first_name and last_name in User if any, otherwise create new
            random_first_name = fake.first_name() if not random_user.first_name else random_user.first_name
            random_last_name = fake.last_name() if not random_user.last_name else random_user.last_name

            # create fake customer
            created_customer = Customer.objects.create(
                user=random_user,
                first_name=random_first_name,
                last_name=random_last_name,
                job=fake.job(),
                notes=fake.paragraph(nb_sentences=3),
                dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
                status=Provider.get_customer_status(random_user)  # status matches the user status
            )

            # assign user email as a contact to the customer
            Contact.objects.create(
                customer=created_customer,
                email=created_customer.user.email,
                phone='',
                note=fake.paragraph(nb_sentences=3),
                type=1
            )

            # assign extra email to some customers
            should_create_email = bool(getrandbits(1))
            if should_create_email:
                random_user_name = Provider.get_random_user_name(fake.first_name())
                Contact.objects.create(
                    customer=created_customer,
                    email=random_user_name + "@gmail.com",
                    note=fake.paragraph(nb_sentences=3),
                    type=1
                )

            # assign phone as a contact to the customer
            random_phone = int("1" + str(fake.msisdn()[3:]))
            Contact.objects.create(
                customer=created_customer,
                email='',
                phone=random_phone,
                note=fake.paragraph(nb_sentences=3),
                type=2
            )

            # assign extra phone to some customers
            should_create_phone = bool(getrandbits(1))
            if should_create_phone:
                random_phone = int("1" + str(fake.msisdn()[3:]))
                Contact.objects.create(
                    customer=created_customer,
                    email='',
                    phone=random_phone,
                    note=fake.paragraph(nb_sentences=3),
                    type=2
                )

        # ----- create leads
        for _ in range(total_leads):

            #  create name for lead
            random_first_name = fake.first_name()
            random_last_name = fake.last_name()

            # create fake lead
            created_lead = Lead.objects.create(
                first_name=random_first_name,
                last_name=random_last_name,
                source=fake.get_random_source(),
                notes=fake.paragraph(nb_sentences=3),
                dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
            )

            # assign email to lead
            random_user_name = Provider.get_random_user_name(created_lead.first_name)
            Contact.objects.create(
                lead=created_lead,
                email=random_user_name + "@gmail.com",
                note=fake.paragraph(nb_sentences=3),
                type=1
            )

            # assign phone to some leads
            should_create_phone = bool(getrandbits(1))
            if should_create_phone:
                random_phone = int("1" + str(fake.msisdn()[3:]))
                Contact.objects.create(
                    lead=created_lead,
                    email='',
                    phone=random_phone,
                    note=fake.paragraph(nb_sentences=3),
                    type=2
                )

        # ----- create vehicles
        for _ in range(total_vehicles):

            # select user for the vehicle
            random_customer = fake.unique.get_random_customer()

            # create fake vehicle
            Vehicle.objects.create(
                customer=random_customer,
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

        # ----- create services
        services_to_be_created = [
            ('self-managed transfer', 255.00, 1, 1),
            ('leasecosts managed transfer', 895.00, 1, 1),
            ('sale', 895.00, 2, 2),
        ]
        for service_data in services_to_be_created:

            # unpack
            name, cost = service_data[0], service_data[1]
            when_to_pay, service_type = service_data[2], service_data[3]

            # create service
            Service.objects.create(
                name=name,
                cost=cost,
                when_to_pay=when_to_pay,
                service_type=service_type,
                description=fake.paragraph(nb_sentences=3)
            )
