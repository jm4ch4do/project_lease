from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from app_lease.models.customer import Customer
from app_lease.models.contact import Contact
from django.contrib.auth.models import User
from datetime import datetime
from random import randint, getrandbits


class Provider(faker.providers.BaseProvider):

    def get_random_customer_status(self):
        return self.random_element(Customer.CHOICES_CUSTOMER_STATUS)[0]

    @staticmethod
    def get_customer_status(user):
        status = 1 if user.is_active else 2
        return status

    def get_random_contact_type(self):
        return self.random_element(Contact.CHOICES_CONTACT_TYPE)

    def get_random_user_id(self):
        users = User.objects.all()
        return self.random_element(users)

    @staticmethod
    def get_random_user_name(first_name):
        number = randint(100, 999)
        username = first_name.lower() + str(number)
        return username


class Command(BaseCommand):

    help = "Command Information"

    def handle(self, *args, **kwargs):

        TOTAL_USERS = 100

        # register customer functions
        fake = Faker()
        fake.add_provider(Provider)

        # delete all customers
        Customer.objects.all().delete()

        # delete all users except superuser
        User.objects.filter(is_superuser=False).delete()

        # generate users
        for _ in range(TOTAL_USERS):

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

        # get all user ids
        total_users = User.objects.all().count()

        # create one customer per user
        for _ in range(TOTAL_USERS):

            # use any username with no repetition
            random_user = fake.unique.get_random_user_id()

            # use first_name and last_name in User if any, otherwise create new
            random_first_name = fake.first_name() if not random_user.first_name else random_user.first_name
            random_last_name = fake.last_name() if not random_user.last_name else random_user.last_name

            # create fake customer
            Customer.objects.create(
                user=random_user,
                first_name=random_first_name,
                last_name=random_last_name,
                notes=fake.paragraph(nb_sentences=3),
                dob=fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
                status=Provider.get_customer_status(random_user)  # status matches the user status
            )
