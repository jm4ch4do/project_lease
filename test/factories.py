from faker import Faker
from django.contrib.auth.models import User
import factory
from app_lease.models import Customer
from datetime import datetime

fake = Faker()


# attach User model to a User Factory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.first_name().lower()
    is_staff = 'True'


# attach Customer model to a Customer Factory
random_first_name = fake.first_name()
random_last_name = fake.last_name()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory),
    first_name = random_first_name,
    last_name = random_last_name,
    job = fake.job(),
    notes = fake.paragraph(nb_sentences=3),
    dob = fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
    status = 1




