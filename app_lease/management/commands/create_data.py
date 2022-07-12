from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers
from app_lease.models.customer import Customer
from app_lease.models.contact import Contact
from django.contrib.auth.models import User
from datetime import datetime


class Provider(faker.providers.BaseProvider):

    def get_random_customer_status(self):
        return self.random_element(Customer.CHOICES_CUSTOMER_STATUS)[0]

    def get_random_contact_type(self):
        return self.random_element(Contact.CHOICES_CONTACT_TYPE)

    def get_random_user_id(self):
        users = User.objects.all()
        return self.random_element(users)


class Command(BaseCommand):

    help = "Command Information"

    def handle(self, *args, **kwargs):

        # register customer functions
        fake = Faker()
        fake.add_provider(Provider)

        # delete all customers
        Customer.objects.all().delete()

        # get all user ids
        total_users = User.objects.all().count()

        # create one customer per user
        for _ in range(total_users):

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
                status=fake.get_random_customer_status(),
            )
