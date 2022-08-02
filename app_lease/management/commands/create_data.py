from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from app_lease.models import *
from django.contrib.auth.models import User
from datetime import datetime
from random import getrandbits
from app_lease.utils.fake_provider import Provider
from random import randint, uniform


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
        Proposal.objects.all().delete()
        Invoice.objects.all().delete()
        CreditCard.objects.all().delete()

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

            # assign credit card to customer
            CreditCard.objects.create(
                customer=created_customer,
                name_in_card=created_customer.first_name + ' ' + created_customer.last_name,
                provider=fake.credit_card_provider(),
                expire_month=randint(1, 12),
                expire_year=randint(datetime.today().year, datetime.today().year + 5),
                security_code=fake.credit_card_security_code(),
                card_number=fake.credit_card_number(),
            )

            # assign a second credit card to some customers
            if randint(1, 2) == 1:
                CreditCard.objects.create(
                    customer=created_customer,
                    name_in_card=fake.name(),
                    provider=fake.credit_card_provider(),
                    expire_month=randint(1, 12),
                    expire_year=randint(datetime.today().year, datetime.today().year + 5),
                    security_code=fake.credit_card_security_code(),
                    card_number=fake.credit_card_number(),
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

        # ----- create one trade per vehicle
        for _ in range(total_vehicles):

            # use any vehicle with no repetition
            selected_vehicle = fake.unique.get_random_vehicle()
            selected_service = fake.get_random_service()

            created_trade = Trade.objects.create(
                service=selected_service,
                vehicle=selected_vehicle,
                note=fake.paragraph(nb_sentences=3),
                status=randint(1, 3)
            )

            # An invoice should be created for service type lease,
            if selected_service.service_type == 1:
                Invoice.objects.create(
                    trade=created_trade,
                    customer=created_trade.vehicle.customer,
                    amount=selected_service.cost,
                    system_note='for creating trade type lease'
                )

        # ----- create one proposal per trade
        # ----- invoices are created in here too when accepting proposals
        for _ in range(total_vehicles):

            # use any trade with no repetition
            selected_trade = fake.unique.get_random_trade()

            # half of the proposals coming from owner, the rest from buyers
            if randint(1, 2) == 1:
                selected_customer = selected_trade.vehicle.customer
            else:
                selected_customer = fake.unique.get_random_customer_not_owner()

            # proposal parameters
            total_amount = round(uniform(10_000, 40_000), 0)
            down_payment = total_amount if selected_trade.service.service_type == 2 else total_amount / 5
            total_days_to_pay = 0 if selected_trade.service.service_type == 2 else randint(90, 1080)
            pay_frequency = 1 if selected_trade.service.service_type == 2 else randint(2, 4)

            created_proposal = Proposal.objects.create(
                trade=selected_trade,
                created_by_customer=selected_customer,
                total_amount=total_amount,
                down_payment=down_payment,
                total_days_to_pay=total_days_to_pay,
                pay_frequency=pay_frequency,
            )

        # ----- accept, cancel or leave open proposals randomly
        for i in range(total_vehicles):

            # select trade and proposal for modifying status
            selected_trade = Trade.objects.all()[i]
            total = selected_trade.proposal_set.all().count()
            proposal_number = randint(1, total)
            selected_proposal = selected_trade.proposal_set.all()[proposal_number-1]

            # randomly modify the status
            choice = randint(1, 3)

            # leave proposal open
            if choice == 1:

                # some open trades will have a refused proposal
                # a proposal can only be refused if it was submitted by buyer
                if selected_proposal.proposed_by == "buyer":
                    selected_proposal.refuse_proposal()

            # cancel proposal
            elif choice == 2:

                # a proposal can only be canceled if it was submitted by owner
                if selected_proposal.proposed_by == "owner":
                    selected_proposal.cancel_proposal()

            # accept proposal
            elif choice == 3:
                if selected_proposal.proposed_by == "buyer":
                    owner = selected_proposal.trade.vehicle.customer
                    selected_proposal.accept_proposal(owner)

                elif selected_proposal.proposed_by == "owner":
                    buyer = fake.get_random_customer_not_owner()
                    selected_proposal.accept_proposal(buyer)
