import faker.providers
from app_lease.models import Customer, Contact, Vehicle, Service, Trade
from django.contrib.auth.models import User
from random import randint


class Provider(faker.providers.BaseProvider):

    def get_random_customer_status(self):
        return self.random_element(Customer.CHOICES_CUSTOMER_STATUS)[0]

    def get_random_source(self):

        SOURCES = ['www.facebook.com', 'www.instagram.com', 'www.tiktok.com', 'www.twitter.com',
                   'www.company1.com', 'www.company2.com', 'www.company3.com', 'www.company4.com']

        return self.random_element(SOURCES)

    @staticmethod
    def get_customer_status(user):
        status = 1 if user.is_active else 2
        return status

    def get_random_contact_type(self):
        return self.random_element(Contact.CHOICES_CONTACT_TYPE)

    def get_random_customer(self):
        customers = Customer.objects.all()
        return self.random_element(customers)

    def get_random_customer_not_owner(self):
        query = "SELECT * FROM app_lease_customer alc WHERE id NOT IN ( SELECT customer_id FROM app_lease_vehicle )"
        customers_not_owners = Customer.objects.raw(query)
        return self.random_element(customers_not_owners)

    def get_random_service(self):
        services = Service.objects.all()
        return self.random_element(services)

    def get_random_trade(self):
        services = Trade.objects.all()
        return self.random_element(services)

    def get_random_user(self):
        users = User.objects.all()
        return self.random_element(users)

    def get_random_vehicle(self):
        vehicles = Vehicle.objects.all()
        return self.random_element(vehicles)

    @staticmethod
    def get_random_user_name(first_name):
        number = randint(100, 999)
        username = first_name.lower() + str(number)
        return username
